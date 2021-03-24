from django import forms

from meinberlin.apps.users.models import User


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'get_notifications', 'get_newsletters']

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username__iexact=username)
            if user != self.instance:
                raise forms.ValidationError(
                    User._meta.get_field('username').error_messages['unique'])
        except User.DoesNotExist:
            pass

        try:
            user = User.objects.get(email__iexact=username)
            if user != self.instance:
                raise forms.ValidationError(User._meta.get_field('username').
                                            error_messages['used_as_email'])
        except User.DoesNotExist:
            pass

        return username
