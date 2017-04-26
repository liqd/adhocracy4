import osa
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from allauth.socialaccount import providers
from allauth.socialaccount.models import SocialLogin, SocialToken
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.helpers import render_authentication_error
from allauth.socialaccount.providers.base import AuthError

from .provider import ServiceKontoProvider


class ServiceKontoApiError(Exception):
    pass


def login(request):
    SocialLogin.stash_state(request)
    return HttpResponseRedirect(settings.SERVICE_KONTO_LOGIN_URL)


@csrf_exempt
def callback(request):
    token = request.GET.get('Token', '')
    if not token:
        return render_authentication_error(
            request, ServiceKontoProvider.id, error=AuthError.UNKNOWN)
    complete_login()


def complete_login(request, token):
    provider = providers.registry.by_id(ServiceKontoProvider.id, request)
    try:
        service_konto = osa.Client(service_konto_url)
    except AttributeError:
        raise ValueError('Failed connecting to ServiceKonto.')
    response = service_konto.service.GetUserData(token)
    response = requests.get(ACCESS_TOKEN_URL, {
        'action': 'authorize',
        'app': app.secret,
        'code': code
    })
    response.raise_for_status()
    response_json = response.json()

    if 'error' in response_json:
        raise DraugiemApiError(response_json['error'])

    token = SocialToken(app=app, token=response_json['apikey'])

    login = provider.sociallogin_from_response(request, response_json)
    login.token = token
    return login
