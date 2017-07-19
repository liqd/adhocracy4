from django import forms

from meinberlin.apps.users.models import User


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'get_notifications']
