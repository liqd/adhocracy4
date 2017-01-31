from django.views import generic
from rules.contrib.views import PermissionRequiredMixin \
    as RulesPermissionRequiredMixin

"""
Common views.

"""


class PermissionRequiredMixin(RulesPermissionRequiredMixin):

    @property
    def raise_exception(self):
        """
        Raises authentication error instead of redirecting to login.

        Needed, as permissions for a logged-in user might still be
        limited by the current phase.
        """
        return self.request.user.is_authenticated()


class SortableListView(generic.ListView):
    """
    ordering_current: List of possible ordering tuples (ordering,
        ordering name).
    """
    orderings_supported = []

    def get_ordering(self):
        ordering = self.request.GET.get('ordering')
        if ordering and ordering in dict(self.orderings_supported):
            self.ordering = [ordering]
        return self.ordering

    def get_current_ordering_name(self):
        return dict(self.orderings_supported)[self.ordering[0]]
