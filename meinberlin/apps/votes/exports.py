from django.utils import timezone
from django.utils.translation import gettext as _
from django.views import generic
from rules.contrib.views import PermissionRequiredMixin

from adhocracy4.exports.views import AbstractXlsxExportView
from adhocracy4.projects.mixins import ProjectMixin
from meinberlin.apps.votes.models import VotingToken

PAGE_SIZE = 1000000


class TokenExportView(PermissionRequiredMixin,
                      ProjectMixin,
                      generic.list.MultipleObjectMixin,
                      AbstractXlsxExportView):
    model = VotingToken
    permission_required = 'a4projects.change_project'
    paginate_by = PAGE_SIZE

    def get_permission_object(self):
        return self.module.project

    def get_queryset(self):
        """Filter QS to only include active tokens from module."""
        return super().get_queryset().filter(
            module=self.module,
            is_active=True
        ).order_by('pk')

    def get_base_filename(self):
        return '%s_%s' % (self.project.slug,
                          timezone.now().strftime('%Y%m%dT%H%M%S'))

    def get_header(self):
        return [_('Voting codes'), ]

    def export_rows(self):
        queryset = self.get_queryset()
        page_size = self.get_paginate_by(queryset)
        _, _, queryset, _ = self.paginate_queryset(
            queryset, page_size
        )
        for item in queryset:
            yield [self.get_token_data(item)]

    def get_token_data(self, item):
        """Add dashes like in string method."""
        return str(item)

    @property
    def raise_exception(self):
        return self.request.user.is_authenticated
