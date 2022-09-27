from math import ceil

from django.conf import settings
from django.contrib import messages
from django.contrib.humanize.templatetags.humanize import intcomma
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from django.utils.translation import ngettext
from django.views import generic
from rules.contrib.views import PermissionRequiredMixin

from adhocracy4.dashboard import mixins as dashboard_mixins
from adhocracy4.exports.views import AbstractXlsxExportView
from adhocracy4.projects.mixins import ProjectMixin
from meinberlin.apps.votes.forms import TokenBatchCreateForm
from meinberlin.apps.votes.models import VotingToken
from meinberlin.apps.votes.tasks import generate_voting_tokens

PAGE_SIZE = 1000000
TOKENS_PER_MODULE = int(5e6)


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
        context['number_of_module_tokens'] = \
            intcomma(self._get_number_of_tokens())
        context['contact_email'] = settings.CONTACT_EMAIL
        context['export_size'] = intcomma(PAGE_SIZE)
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
        """Add dashes like in string method."""
        return str(item)

    @property
    def raise_exception(self):
        return self.request.user.is_authenticated


class VotingGenerationDashboardView(
        ProjectMixin, dashboard_mixins.DashboardBaseMixin,
        dashboard_mixins.DashboardComponentMixin,
        generic.base.TemplateResponseMixin, generic.edit.FormMixin,
        generic.edit.ProcessFormView):
    model = VotingToken
    form_class = TokenBatchCreateForm
    success_message = (
        _('{} code will be generated in the background. '
          'This may take a few minutes.'),
        _('{} codes will be generated in the background. '
          'This may take a few minutes.'))
    error_message_token_number = (
        _('Please adjust your number of codes. Per module you can '
          'generate up to {} codes.'))
    permission_required = 'is_superuser'
    template_name = 'meinberlin_votes/voting_code_dashboard.html'

    def _get_number_of_tokens(self):
        return VotingToken.objects.filter(
            module=self.module,
            is_active=True
        ).count()

    def get_permission_object(self):
        return self.project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['number_of_module_tokens'] = \
            intcomma(self._get_number_of_tokens())
        context['tokens_per_module'] = intcomma(TOKENS_PER_MODULE)
        return context

    def get_success_url(self):
        return reverse(
            'a4dashboard:voting-token-generation',
            kwargs={'module_slug': self.module.slug})

    def form_valid(self, form):
        number_of_tokens = form.cleaned_data['number_of_tokens']
        # check that no more than 5 Million codes are added per module
        existing_tokens = self._get_number_of_tokens()
        if existing_tokens + number_of_tokens > TOKENS_PER_MODULE:
            messages.error(
                self.request,
                self.error_message_token_number.format(
                    intcomma(TOKENS_PER_MODULE)
                )
            )
        else:
            # make tasks to generate the tokens
            generate_voting_tokens(self.module.pk, number_of_tokens)

            messages.success(
                self.request,
                ngettext(self.success_message[0], self.success_message[1],
                         number_of_tokens).format(intcomma(number_of_tokens))
            )

        return redirect(self.get_success_url())
