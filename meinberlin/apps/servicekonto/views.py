from xml.etree import ElementTree

import requests
import zeep
from allauth.socialaccount import providers
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.helpers import render_authentication_error
from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.providers.base import AuthError
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .provider import ServiceKontoProvider

SERVICE_KONTO_GET_USER_DATA_SUCCESS = 1


class ServiceKontoApiError(Exception):
    def __init__(self, error=AuthError.UNKNOWN):
        self.error = error


def login(request):
    login_redirect_url = reverse("servicekonto_login_redirect")
    if request.GET:
        login_redirect_url = login_redirect_url + "?" + request.GET.urlencode()

    return render(
        request,
        "meinberlin_servicekonto/login.html",
        context={"login_redirect_url": login_redirect_url},
    )


def login_redirect(request):
    SocialLogin.stash_state(request)
    return HttpResponseRedirect(settings.SERVICE_KONTO_LOGIN_URL)


@csrf_exempt
def callback(request):
    token = request.POST.get("Token", "")
    if not token:
        return render_authentication_error(
            request, ServiceKontoProvider.id, error=AuthError.UNKNOWN
        )

    try:
        login = _complete_login(request, token)
    except ServiceKontoApiError as e:
        return render_authentication_error(
            request, ServiceKontoProvider.id, exception=e.__cause__, error=e.error
        )
    except ValueError as e:
        return render_authentication_error(
            request, ServiceKontoProvider.id, exception=e, error=AuthError.UNKNOWN
        )

    ret = complete_social_login(request, login)
    if not ret:
        ret = render_authentication_error(request, ServiceKontoProvider.id)

    return ret


def _complete_login(request, token):
    user_data_xml = _get_service_konto_user_data_xml(request, token)
    user_data = _parse_user_data_xml(user_data_xml)

    provider = providers.registry.by_id(ServiceKontoProvider.id, request)
    login = provider.sociallogin_from_response(request, user_data)
    login.state = _unstash_state(request)
    return login


def _unstash_state(request):
    """Return the state if it exists."""
    if "socialaccount_state" in request.session:
        return SocialLogin.unstash_state(request)
    return {}


def _get_service_konto_user_data_xml(request, token):
    transport = None
    cert = getattr(settings, "SERVICE_KONTO_CERT", None)
    if cert:
        session = requests.Session()
        session.cert = cert
        transport = zeep.transports.Transport(session=session)
    service_konto = zeep.Client(settings.SERVICE_KONTO_API_URL, transport=transport)

    result = service_konto.service.GetUserData(token)
    if not result.GetUserDataResult == SERVICE_KONTO_GET_USER_DATA_SUCCESS:
        raise ServiceKontoApiError(error=AuthError.DENIED)

    return result.strXMLUserData


def _parse_user_data_xml(xml: str) -> dict:
    try:
        root = ElementTree.fromstring(xml)
    except ElementTree.ParseError as e:
        raise ValueError("Invalid XML received") from e

    hhgw = root.find("./HHGW")
    if hhgw is None:
        raise ValueError("Invalid data received.")

    user_data = {key.lower(): value for key, value in hhgw.attrib.items()}
    if not _is_user_data_valid(user_data):
        raise ValueError("Invalid user data received.")
    return user_data


def _is_user_data_valid(user_data: dict) -> bool:
    return (
        user_data.get("userid")
        and user_data.get("loginname")
        and user_data.get("email")
        and user_data.get("levelid")
    )
