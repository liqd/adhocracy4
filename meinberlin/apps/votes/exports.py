from django.core.exceptions import BadRequest
from django.utils.translation import gettext as _
from django.views import generic
from rules.contrib.views import PermissionRequiredMixin

from adhocracy4.exports.views import AbstractXlsxExportView
from adhocracy4.projects.mixins import ProjectMixin
from meinberlin.apps.votes.models import VotingToken


class TokenExportView(
    PermissionRequiredMixin,
    ProjectMixin,
    generic.list.MultipleObjectMixin,
    AbstractXlsxExportView,
):
    model = VotingToken
    permission_required = "a4projects.change_project"

    def get_permission_object(self):
        return self.module.project

    def get_package_number(self):
        package_number = self.request.GET.get("package") or 0
        try:
            return int(package_number)
        except ValueError:
            return None

    def get_queryset(self):
        """Filter QS to only include active tokens from module."""
        package_number = self.get_package_number()
        if package_number is None:
            return None
        return (
            super()
            .get_queryset()
            .filter(module=self.module, is_active=True, package_number=package_number)
            .exclude(token="")
            .order_by("pk")
        )

    def get_base_filename(self):
        package_number = self.get_package_number()
        if not package_number:
            package_number = 0
        return "%s_package_%s" % (self.project.slug, package_number)

    def get_header(self):
        return [
            _("Voting codes"),
        ]

    def export_rows(self):
        queryset = self.get_queryset()
        # raise BadRequest as either package has been downloaded
        # already or wrong package number
        if queryset is None or queryset.count() == 0:
            raise BadRequest
        for item in queryset:
            yield [self.get_token_data(item)]
        queryset.update(token="")

    def get_token_data(self, item):
        """Add dashes like in string method."""
        return str(item)

    @property
    def raise_exception(self):
        return self.request.user.is_authenticated
