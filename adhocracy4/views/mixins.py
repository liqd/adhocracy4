from rules.contrib.views import PermissionRequiredMixin \
    as RulesPermissionRequiredMixin

"""
Common mixins.

"""


class PermissionRequiredMixin(RulesPermissionRequiredMixin):

    @property
    def raise_exception(self):
        """Raise authentication error instead of redirecting to login.

        Needed, as permissions for a logged-in user might still be
        limited by the current phase.
        """
        return self.request.user.is_authenticated()
