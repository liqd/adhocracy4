from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.forms.fields import Field
from django.forms.widgets import EmailInput

from apps.users.models import User


class UserField(Field):

    def __init__(self, *args, **kwargs):
        self.widget = EmailInput
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if value:
            try:
                return User.objects.get(email__exact=value)
            except ObjectDoesNotExist:
                raise ValidationError('{} doesn\'t exist.'.format(value))
        return None
