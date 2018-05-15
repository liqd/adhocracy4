from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class TermsSignupForm(auth_forms.UserCreationForm):
    terms_of_use = forms.BooleanField(label=_('Terms of use'), error_messages={
        'required': _('Please accept the terms of use.')
    })

    def signup(self, request, user):
        user.signup(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
        )

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2',
                  'terms_of_use')
