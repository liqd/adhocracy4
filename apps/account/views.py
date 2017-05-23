from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views import generic
from django.views.generic.base import RedirectView

from apps.users.models import User
from . import forms


class AccountView(RedirectView):
    pattern_name = 'account_profile'
    # Placeholder View to be replaced if we want to use a custom account
    # dashboard function overview.


class ProfileUpdateView(SuccessMessageMixin,
                        generic.UpdateView):

    model = User
    template_name = "meinberlin_account/profile.html"
    form_class = forms.ProfileForm
    success_message = _("Your profile was successfully updated.")

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.id)

    def get_success_url(self):
        return self.request.path
