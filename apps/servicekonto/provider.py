from django.core.urlresolvers import reverse
from django.utils.http import urlencode

from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import Provider
from allauth.socialaccount.providers.base import ProviderAccount


class ServiceKontoAccount(ProviderAccount):
    pass


class ServiceKontoProvider(Provider):
    id = 'servicekonto'
    name = 'ServiceKonto'
    account_class = ServiceKontoAccount

    def get_login_url(self, request, **kwargs):
        url = reverse(self.id + "_login")
        if kwargs:
            url = url + '?' + urlencode(kwargs)
        return url

providers.registry.register(ServiceKontoProvider)
