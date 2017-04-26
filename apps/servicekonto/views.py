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
    pass


def complete_login(request, app, code):
    pass
