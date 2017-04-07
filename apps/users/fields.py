import re
from django.core.validators import RegexValidator
from django.forms.fields import Field
from django.forms.widgets import Textarea


class CommaSeparatedEmailField(Field):
    default_validators = [RegexValidator(
        # a list of emails, separated by commas with optional space after
        regex=r'^([^@]+@[^@\s]+\.[^@\s,]+((,\s?)|$))+$',
        # message=_('Please enter correct e-mail addresses, separated by '
        #          'commas.')
    )]

    widget = Textarea(attrs={
        'placeholder': 'jana@beispiel.de, tobias@beispiel.de, '
                       'swetlana@beispiel.de,…'
    })

    def to_python(self, value):
        emails_str = value.strip(' ,')
        return re.split(r',\s?', emails_str)


"""
class ProjectInviteForm(forms.Form):
    def __init__(self, project, *args, **kwargs):
        self.project = project
        super().__init__(*args, **kwargs)

    def clean_emails(self):
        emails_str = self.cleaned_data['emails'].strip(' ,')
        emails = re.split(r',\s?', emails_str)

        query = {
            'project': self.project,
            'email__in': emails,
        }
        existing = member_models.Invite.objects.filter(**query)\
                                               .values_list('email', flat=True)
        if existing:
            for address in existing:
                raise ValidationError(
                    '{} already invited'.format(address)
                )

        return emails
"""
