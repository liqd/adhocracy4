from django.utils.translation import ugettext_lazy as _


USERNAME_REGEX = r'^[\w]+[ \w.@+-]*$'
USERNAME_INVALID_MESSAGE = _('Enter a valid username. This value may contain '
                             'only letters, digits, spaces and @/./+/-/_ '
                             'characters. It must start with a digit or a '
                             'letter.')
