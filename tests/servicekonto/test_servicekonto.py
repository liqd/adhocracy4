from urllib.parse import urlparse

import pytest

from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.providers.base import AuthProcess
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.test import RequestFactory

from apps.servicekonto.provider import ServiceKontoProvider

User = get_user_model()


def _mock_servicekonto_response(monkeypatch, response):
    monkeypatch.setattr(
        'apps.servicekonto.views._get_service_konto_user_data_xml',
        lambda request, token: str(response)
    )


def _session_state(client, data):
    rf = RequestFactory()

    redirect_url = reverse('servicekonto_login_redirect')
    request = rf.get(redirect_url, data)

    session = client.session
    state = SocialLogin.state_from_request(request)
    verifier = 0
    session['socialaccount_state'] = (state, verifier)
    session.save()


class ServiceKontoResponse:
    hhgw = {
        'userid': '1',
        'modeid': '1',
        'usermode': 'Bürger',
        'loginname': 'user@liqd.de',
        'title': '',
        'prefix': 'Herr',
        'firstname': 'Max',
        'lastname': 'Mustermann',
        'email': 'user@liqd.de',
        'language': 'de-DE',
        'levelid': '1',
        'street': '',
        'streetnumber': '',
        'streetextension': '',
        'city': '',
        'zipcode': '',
        'country': 'Deutschland',
        'dateofbirth': '',
        'certificated': '',
        'userphonenumber': '',
    }

    roles = {
        'roleid': '991',
        'rolename': 'Standard',
        'permission': '1',
        'isdefault': '1'
    }

    authentication = {
        'AuthenticationModeID': '1',
        'InvalidAt': '2100-01-01T00:00:00.000'
    }

    def __init__(self, hhgw=None, roles=None, authentication=None):
        if hhgw:
            self.hhgw.update(hhgw)
        if roles:
            self.roles.update(roles)
        if authentication:
            self.roles.update(authentication)

    @classmethod
    def _dict_to_string(cls, d, upper=True):
        return ' '.join('{}="{}"'.format(key.upper() if upper else key, value)
                        for key, value in d.items())

    def __str__(self):
        ctx = dict(hhgw=self._dict_to_string(self.hhgw),
                   roles=self._dict_to_string(self.roles),
                   authentication=self._dict_to_string(self.authentication,
                                                       False))
        return '<USERDATA><HHGW {hhgw} /><ROLES {roles} />' \
               '<AUTHENTICATION {authentication} /></USERDATA>'.format(**ctx)


@pytest.mark.django_db
def test_connect_account(monkeypatch, client, user):
    client.login(email=user.email, password='password')
    _session_state(client, {'process': AuthProcess.CONNECT})

    service_konto = ServiceKontoResponse(
        hhgw={'email': user.email}
    )
    _mock_servicekonto_response(monkeypatch, service_konto)

    response = client.get(reverse('servicekonto_callback'),
                          {'Token': '1234567'})
    assert response.status_code == 302

    account = SocialAccount.objects.get(
        user=user,
        provider=ServiceKontoProvider.id
    )
    assert account.uid == service_konto.hhgw['userid']


@pytest.mark.django_db
def test_login(monkeypatch, client, social_account):
    _session_state(client, {'process': AuthProcess.LOGIN,
                            'next': '/login_session_successful'})
    user = social_account.user

    service_konto = ServiceKontoResponse(
        hhgw={'email': user.email,
              'userid': social_account.uid}
    )
    _mock_servicekonto_response(monkeypatch, service_konto)

    response = client.get(reverse('servicekonto_callback'),
                          {'Token': '1234567'})
    assert response.status_code == 302

    response_url = urlparse(response.url)
    assert response_url.path == '/login_session_successful'


@pytest.mark.django_db
def test_login_without_session(monkeypatch, client, social_account, settings):
    settings.LOGIN_REDIRECT_URL = '/login_successful'
    user = social_account.user

    service_konto = ServiceKontoResponse(
        hhgw={'email': user.email,
              'userid': social_account.uid}
    )
    _mock_servicekonto_response(monkeypatch, service_konto)

    response = client.get(reverse('servicekonto_callback'),
                          {'Token': '1234567'})
    assert response.status_code == 302

    response_url = urlparse(response.url)
    assert response_url.path == '/login_successful'


@pytest.mark.django_db
def test_create_account_on_login(monkeypatch, client, settings):
    settings.LOGIN_REDIRECT_URL = '/login_successful'

    service_konto = ServiceKontoResponse()
    _mock_servicekonto_response(monkeypatch, service_konto)

    response = client.get(reverse('servicekonto_callback'),
                          {'Token': '1234567'})
    assert response.status_code == 302

    response_url = urlparse(response.url)
    assert response_url.path == '/login_successful'

    user = User.objects.get(email=service_konto.hhgw['email'])
    assert user.pk

    emails = user.emailaddress_set
    assert emails.count() == 1

    email = emails.first()
    assert email.email == service_konto.hhgw['email']
    assert email.primary
    assert email.verified


@pytest.mark.django_db
def test_create_account_on_login_with_existing_username(monkeypatch,
                                                        client,
                                                        user_factory,
                                                        settings):
    settings.LOGIN_REDIRECT_URL = '/login_successful'

    user_factory(username='first_last')
    service_konto = ServiceKontoResponse(
        hhgw={'firstname': 'first', 'lastname': 'last'})
    _mock_servicekonto_response(monkeypatch, service_konto)

    response = client.get(reverse('servicekonto_callback'),
                          {'Token': '1234567'})
    assert response.status_code == 302

    response_url = urlparse(response.url)
    assert response_url.path == '/login_successful'

    user = User.objects.get(email=service_konto.hhgw['email'])
    assert user.pk


@pytest.mark.django_db
def test_skip_create_if_exists(monkeypatch, client, user_factory, settings):
    settings.LOGIN_REDIRECT_URL = '/login_successful'

    email_address = 'duplicated@liqd.de'
    user_factory(email=email_address)
    service_konto = ServiceKontoResponse(hhgw={'email': email_address})
    _mock_servicekonto_response(monkeypatch, service_konto)

    response = client.get(reverse('servicekonto_callback'),
                          {'Token': '1234567'})
    assert response.status_code == 302

    response_url = urlparse(response.url)
    assert response_url.path != '/login_successful'

    with pytest.raises(ObjectDoesNotExist):
        SocialAccount.objects.get(
            uid=service_konto.hhgw['userid'],
            provider=ServiceKontoProvider.id
        )


# @pytest.mark.django_db
# def test_invalid_token(monkeypatch, client):
#     def auth_denied(request, token):
#         raise views.ServiceKontoApiError(error=AuthError.DENIED)
#
#     monkeypatch.setattr(
#         'apps.servicekonto.views._get_service_konto_user_data_xml',
#         auth_denied
#     )
#
#     response = client.get(reverse('servicekonto_callback'),
#                           {'Token': ''})
#     assert response.status_code == 500
#
#
#
# @pytest.mark.django_db
# def test_invalid_response(monkeypatch, client):
#     _mock_servicekonto_response(monkeypatch, '<invalid>xml response')
#     response = client.get(reverse('servicekonto_callback'),
#                           {'Token': ''})
#     assert response.status_code == 500
