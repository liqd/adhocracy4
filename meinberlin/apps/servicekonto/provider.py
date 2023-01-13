from allauth.socialaccount.providers.base import Provider
from allauth.socialaccount.providers.base import ProviderAccount
from django.urls import reverse
from django.utils.http import urlencode


class ServiceKontoAccount(ProviderAccount):
    def to_str(self):
        return "%s" % (self.account.extra_data["email"])


class ServiceKontoProvider(Provider):
    id = "servicekonto"
    name = "Service-Konto"
    account_class = ServiceKontoAccount

    def get_login_url(self, request, **kwargs):
        url = reverse(self.id + "_login")
        if kwargs:
            url = url + "?" + urlencode(kwargs)
        return url

    def extract_uid(self, data):
        return data["userid"]

    def extract_common_fields(self, data):
        return {
            "email": data["email"],
            "levelid": data["levelid"],
        }

    def get_settings(self):
        settings = {
            "VERIFIED_EMAIL": True,
        }
        provider_settings = super(ServiceKontoProvider, self).get_settings()
        settings.update(provider_settings)
        return settings
