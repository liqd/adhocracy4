import django_filters
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from adhocracy4.categories import filters as category_filters
from adhocracy4.filters import filters as a4_filters
from adhocracy4.projects.mixins import DisplayProjectOrModuleMixin
from meinberlin.apps.contrib import filters
from meinberlin.apps.exports.views import DashboardExportView
from meinberlin.apps.ideas import views as idea_views
from meinberlin.apps.projects.views import ArchivedWidget

from . import forms
from . import models


def get_ordering_choices(view):
    choices = (('-created', _('Most recent')),)
    if view.module.has_feature('rate', models.Proposal):
        choices += ('-positive_rating_count', _('Most popular')),
    choices += ('-comment_count', _('Most commented')),
    return choices


class ProposalFilterSet(a4_filters.DefaultsFilterSet):
    defaults = {
        'ordering': '-created',
        'is_archived': 'false'
    }
    category = category_filters.CategoryFilter()
    ordering = filters.OrderingFilter(
        choices=get_ordering_choices
    )
    is_archived = django_filters.BooleanFilter(
        widget=ArchivedWidget
    )

    class Meta:
        model = models.Proposal
        fields = ['category', 'is_archived']


class ProposalListView(idea_views.AbstractIdeaListView,
                       DisplayProjectOrModuleMixin):
    model = models.Proposal
    filter_set = ProposalFilterSet

    def dispatch(self, request, **kwargs):
        self.mode = request.GET.get('mode', 'map')
        if self.mode == 'map':
            self.paginate_by = 0
        return super().dispatch(request, **kwargs)

    def get_queryset(self):
        return super().get_queryset()\
            .filter(module=self.module) \
            .annotate_positive_rating_count() \
            .annotate_negative_rating_count() \
            .annotate_comment_count()


class ProposalDetailView(idea_views.AbstractIdeaDetailView):
    model = models.Proposal
    queryset = models.Proposal.objects.annotate_positive_rating_count()\
        .annotate_negative_rating_count()
    permission_required = 'meinberlin_budgeting.view_proposal'


class ProposalCreateView(idea_views.AbstractIdeaCreateView):
    model = models.Proposal
    form_class = forms.ProposalForm
    permission_required = 'meinberlin_budgeting.add_proposal'
    template_name = 'meinberlin_budgeting/proposal_create_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ProposalUpdateView(idea_views.AbstractIdeaUpdateView):
    model = models.Proposal
    form_class = forms.ProposalForm
    permission_required = 'meinberlin_budgeting.change_proposal'
    template_name = 'meinberlin_budgeting/proposal_update_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ProposalDeleteView(idea_views.AbstractIdeaDeleteView):
    model = models.Proposal
    success_message = _('Your budget request has been deleted')
    permission_required = 'meinberlin_budgeting.change_proposal'
    template_name = 'meinberlin_budgeting/proposal_confirm_delete.html'


class ProposalModerateView(idea_views.AbstractIdeaModerateView):
    model = models.Proposal
    permission_required = 'meinberlin_budgeting.moderate_proposal'
    template_name = 'meinberlin_budgeting/proposal_moderate_form.html'
    moderateable_form_class = forms.ProposalModerateForm


class ProposalDashboardExportView(DashboardExportView):
    template_name = 'meinberlin_exports/export_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['export'] = reverse(
            'a4dashboard:budgeting-export',
            kwargs={'module_slug': self.module.slug})
        context['comment_export'] = reverse(
            'a4dashboard:budgeting-comment-export',
            kwargs={'module_slug': self.module.slug})
        return context
