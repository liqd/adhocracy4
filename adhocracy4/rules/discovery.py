import rules


class NormalUser():
    """
    Fake user with same state as freshly registerted user.
    This fake user object is used to check wether a login would help
    to enable an action. This user doesn't have any previliges granted
    except that it is authenticated.
    """
    username = 'NormalUser'
    email = 'noreply@liqd.net'
    password = ''
    is_staff = False
    is_active = True
    is_superuser = False

    def is_authenticated(self):
        return True

    def would_perm(self, perm, obj):
        return rules.has_perm(perm, self, obj)
