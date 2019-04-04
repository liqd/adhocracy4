import rules
from django.contrib.auth.models import AnonymousUser


class NormalUser(AnonymousUser):
    """
    Fake user with same state as freshly registerted user.
    This fake user object is used to check wether a login would help
    to enable an action. This user doesn't have any previliges granted
    except that it is authenticated.
    """

    def __str__(self):
        return 'NormalUser'

    @property
    def is_authenticated(self):
        return True

    def would_have_perm(self, perm, obj):
        return rules.has_perm(perm, self, obj)
