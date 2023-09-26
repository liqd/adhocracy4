from django.core.exceptions import BadRequest
from django.utils.translation import gettext as _
from django.views import generic
from rules.contrib.views import PermissionRequiredMixin

from adhocracy4.exports.views import AbstractXlsxExportView
from adhocracy4.projects.mixins import ProjectMixin
from meinberlin.apps.votes.models import TokenPackage
from meinberlin.apps.votes.models import VotingToken
from meinberlin.apps.votes.tasks import delete_plain_codes


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

    def get_package(self):
        try:
            pk = int(self.request.GET.get("package"))
            return TokenPackage.objects.get(pk=pk)
        except ValueError:
            return None

    def get_queryset(self):
        """Filter QS to only include active tokens from module."""
        package = self.get_package()
        if package is None:
            return None
        return (
            super()
            .get_queryset()
            .filter(
                module=self.module,
                is_active=True,
                package=package,
            )
            .exclude(token="")
            .order_by("pk")
        )

    def get_base_filename(self):
        package = self.get_package()
        package_number = (
            TokenPackage.objects.filter(module=self.module, pk__lt=package.pk).count()
            + 1
        )
        return "%s_package_%s" % (self.project.slug, package_number)

    def get_header(self):
        return [
            _("Voting codes"),
        ]

    def export_rows(self):
        queryset = self.get_queryset()
        # raise BadRequest as either package has been downloaded
        # already or wrong package number
        package = self.get_package()
        if queryset is None or queryset.count() == 0 or not package.is_created:
            raise BadRequest
        for item in queryset:
            yield [self.get_token_data(item)]
        package.downloaded = True
        package.save()
        delete_plain_codes.delay(package.pk)

    def get_token_data(self, item):
        """Add dashes like in string method."""
        return str(item)

    @property
    def raise_exception(self):
        return self.request.user.is_authenticated
