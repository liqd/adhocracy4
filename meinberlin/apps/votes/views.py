from math import ceil

from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views import generic
from rules.contrib.views import PermissionRequiredMixin

from adhocracy4.dashboard import mixins as dashboard_mixins
from adhocracy4.exports.views import AbstractXlsxExportView
from adhocracy4.projects.mixins import ProjectMixin
from meinberlin.apps.votes.models import VotingToken

PAGE_SIZE = 1000000


class VotingDashboardView(ProjectMixin,
                          dashboard_mixins.DashboardBaseMixin,
                          dashboard_mixins.DashboardComponentMixin,
                          generic.TemplateView):
    permission_required = 'a4projects.change_project'
    template_name = 'meinberlin_votes/voting_dashboard.html'

    def _get_number_of_tokens(self):
        return VotingToken.objects.filter(
            module=self.module,
            is_active=True
        ).count()

    def _get_page_range(self):
        number_of_tokens = self._get_number_of_tokens()
        number_of_pages = ceil(number_of_tokens / PAGE_SIZE)
        return range(1, number_of_pages + 1)

    def get_permission_object(self):
        return self.project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['token_export_url'] = reverse(
            'a4dashboard:token-export',
            kwargs={'module_slug': self.module.slug})
        context['token_export_iterator'] = self._get_page_range()
        context['number_of_module_tokens'] = self._get_number_of_tokens()
        return context


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
        return item.token

    @property
    def raise_exception(self):
        return self.request.user.is_authenticated
