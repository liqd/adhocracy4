import django_filters
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from adhocracy4.categories import filters as category_filters
from adhocracy4.exports.views import DashboardExportView
from adhocracy4.filters import filters as a4_filters
from adhocracy4.labels import filters as label_filters
from adhocracy4.projects.mixins import DisplayProjectOrModuleMixin
from meinberlin.apps.ideas import views as idea_views
from meinberlin.apps.moderatorremark.forms import ModeratorRemarkForm
from meinberlin.apps.projects.views import ArchivedWidget
from meinberlin.apps.votes.forms import TokenForm
from meinberlin.apps.votes.models import VotingToken

from . import forms
from . import models


def get_ordering_choices(view):
    choices = (('-created', _('Most recent')),)
    if view.module.has_feature('rate', models.Proposal):
        choices += ('-positive_rating_count', _('Most popular')),
    elif view.module.has_feature('support', models.Proposal):
        choices += ('-positive_rating_count', _('Most support')),
    choices += ('-comment_count', _('Most commented')), \
               ('dailyrandom', _('Random')),
    return choices


class ProposalFilterSet(a4_filters.DefaultsFilterSet):
    defaults = {
        'ordering': '-created',
        'is_archived': 'false'
    }
    category = category_filters.CategoryFilter()
    labels = label_filters.LabelFilter()
    ordering = a4_filters.DistinctOrderingWithDailyRandomFilter(
        choices=get_ordering_choices
    )
    is_archived = django_filters.BooleanFilter(
        widget=ArchivedWidget
    )

    class Meta:
        model = models.Proposal
        fields = ['category', 'labels', 'is_archived']


class ProposalListView(idea_views.AbstractIdeaListView,
                       DisplayProjectOrModuleMixin):
    model = models.Proposal
    filter_set = ProposalFilterSet

    def has_valid_token_in_session(self, request):
        """Return whether a valid token is stored in the session.

        The token is valid if it is valid for the respective module.
        """
        if 'voting_token' in request.session:
            token_queryset = VotingToken.objects.filter(
                token=request.session['voting_token'],
                module=self.module
            )
            return token_queryset.exists()
        return False

    def dispatch(self, request, **kwargs):
        self.mode = request.GET.get('mode', 'map')
        if self.mode == 'map':
            self.paginate_by = 0
        return super().dispatch(request, **kwargs)

    def get_queryset(self):
        return super().get_queryset()\
            .filter(module=self.module)

    def get_context_data(self, **kwargs):
        if 'token_form' not in kwargs:
            token_form = TokenForm(module_id=self.module.id)
            kwargs['token_form'] = token_form
        kwargs['valid_token_present'] = \
            self.has_valid_token_in_session(self.request)
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        token_form = TokenForm(request.POST, module_id=self.module.id)
        if token_form.is_valid():
            request.session['voting_token'] = token_form.cleaned_data['token']
            kwargs['valid_token_present'] = True
            self.mode = 'list'
        kwargs['token_form'] = token_form
        context = super().get_context_data(**kwargs)
        return self.render_to_response(context)


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
    remark_form_class = ModeratorRemarkForm


class ProposalDashboardExportView(DashboardExportView):
    template_name = 'a4exports/export_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['export'] = reverse(
            'a4dashboard:budgeting-export',
            kwargs={'module_slug': self.module.slug})
        context['comment_export'] = reverse(
            'a4dashboard:budgeting-comment-export',
            kwargs={'module_slug': self.module.slug})
        return context
