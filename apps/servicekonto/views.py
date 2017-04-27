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
    complete_login(request, token)


def complete_login(request, token):
    provider = providers.registry.by_id(ServiceKontoProvider.id, request)
    try:
        service_konto = osa.Client(settings.SERVICE_KONTO_API_URL)
    except AttributeError:
        return render_authentication_error(
            request, ServiceKontoProvider.id, error=AuthError.UNKNOWN)
    result = service_konto.service.GetUserData(token)
    login = provider.sociallogin_from_response(request, None)
    login.token = token
    return login
