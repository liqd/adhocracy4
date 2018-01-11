import django_filters
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from adhocracy4.categories import filters as category_filters
from adhocracy4.filters import filters as a4_filters
from adhocracy4.projects.mixins import ProjectMixin
from adhocracy4.rules import mixins as rules_mixins
from meinberlin.apps.contrib import forms as contrib_forms
from meinberlin.apps.contrib import filters
from meinberlin.apps.ideas import views as idea_views
from meinberlin.apps.moderatorfeedback.forms import ModeratorStatementForm
from meinberlin.apps.moderatorfeedback.models import ModeratorStatement
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


class ProposalListView(idea_views.AbstractIdeaListView):
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


class ProposalUpdateView(idea_views.AbstractIdeaUpdateView):
    model = models.Proposal
    form_class = forms.ProposalForm
    permission_required = 'meinberlin_budgeting.change_proposal'
    template_name = 'meinberlin_budgeting/proposal_update_form.html'


class ProposalDeleteView(idea_views.AbstractIdeaDeleteView):
    model = models.Proposal
    success_message = _('Your budget request has been deleted')
    permission_required = 'meinberlin_budgeting.change_proposal'
    template_name = 'meinberlin_budgeting/proposal_confirm_delete.html'


class ProposalModerateView(ProjectMixin,
                           rules_mixins.PermissionRequiredMixin,
                           generic.detail.SingleObjectMixin,
                           generic.detail.SingleObjectTemplateResponseMixin,
                           contrib_forms.BaseMultiModelFormView):
    model = models.Proposal
    permission_required = 'meinberlin_budgeting.moderate_proposal'
    template_name = 'meinberlin_budgeting/proposal_moderate_form.html'
    get_context_from_object = True

    forms = {
        'proposal': {
            'model': models.Proposal,
            'form_class': forms.ProposalModerateForm
        },
        'statement': {
            'model': ModeratorStatement,
            'form_class': ModeratorStatementForm
        }
    }

    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return self.object.get_absolute_url()

    def forms_save(self, forms, commit=True):
        objects = super().forms_save(forms, commit=False)
        proposal = objects['proposal']
        statement = objects['statement']

        if not statement.pk:
            statement.creator = self.request.user

        with transaction.atomic():
            statement.save()
            proposal.moderator_statement = statement
            proposal.save()
        return objects

    def get_instance(self, name):
        if name == 'proposal':
            return self.object
        elif name == 'statement':
            return self.object.moderator_statement
