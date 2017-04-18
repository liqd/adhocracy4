from allauth.account import views as account_views
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views import generic

from apps.users.models import User
from . import forms


class AccountBaseMixin:
    def get_success_url(self):
        return self.request.path


class AccountEmailView(AccountBaseMixin,
                       account_views.EmailView):
    template_name = 'meinberlin_account/email.html'
    menu_item = 'email'


class ProfileUpdateView(AccountBaseMixin,
                        SuccessMessageMixin,
                        generic.UpdateView):

    model = User
    template_name = "meinberlin_account/profile.html"
    form_class = forms.ProfileForm
    success_message = _("Your profile was successfully updated.")
    menu_item = 'profile'

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.id)


class ChangePasswordView(AccountBaseMixin,
                         account_views.PasswordChangeView):
    menu_item = 'password'
    template_name = 'meinberlin_account/password.html'
    menu_item = 'password'
