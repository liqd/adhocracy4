from rules.predicates import is_superuser

from adhocracy4.organisations.predicates import is_initiator


class DashboardProjectListGroupMixin():
    def get_queryset(self, **kwargs):
        qs = super().get_queryset()
        if (is_initiator(self.request.user, self.organisation)
                or is_superuser(self.request.user)):
            return qs
        else:
            return qs.filter(
                group__id__in=[self.request.user.groups.values_list(
                    'id', flat=True)]
            )
