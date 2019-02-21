from rules.contrib import views as rules_views


class PermissionRequiredMixin(rules_views.PermissionRequiredMixin):

    @property
    def raise_exception(self):
        """Raise authentication error instead of redirecting to login.

        Needed, as permissions for a logged-in user might still be
        limited by the current phase.
        """
        return self.request.user.is_authenticated
