import django_filters
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.views import generic

from adhocracy4.modules import views as module_views
from adhocracy4.rules import mixins as rules_mixins
from apps.contrib import filters

from . import forms
from . import models


def get_ordering_choices(request):
    choices = (('-created', _('Most recent')),)
    if request.module.has_feature('rate', models.Proposal):
        choices += ('-positive_rating_count', _('Most popular')),
    choices += ('-comment_count', _('Most commented')),
    return choices


class ProposalFilterSet(django_filters.FilterSet):

    category = filters.CategoryFilter()

    ordering = filters.OrderingFilter(
        choices=get_ordering_choices
    )

    class Meta:
        model = models.Proposal
        fields = ['category']


class ProposalListView(module_views.ItemListView):
    model = models.Proposal
    filter_set = ProposalFilterSet

    def dispatch(self, request, **kwargs):
        self.mode = request.GET.get('mode', 'map')
        if self.mode == 'map':
            self.paginate_by = 0
        return super().dispatch(request, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(module=self.module) \
            .annotate_positive_rating_count() \
            .annotate_negative_rating_count() \
            .annotate_comment_count()


class ProposalDetailView(module_views.ItemDetailView):
    model = models.Proposal
    queryset = models.Proposal.objects.annotate_positive_rating_count()\
        .annotate_negative_rating_count()
    permission_required = 'meinberlin_kiezkasse.view_proposal'


class ProposalCreateView(module_views.ItemCreateView):
    model = models.Proposal
    form_class = forms.ProposalForm
    permission_required = 'meinberlin_kiezkasse.add_proposal'
    template_name = 'meinberlin_kiezkasse/proposal_create_form.html'


class ProposalUpdateView(module_views.ItemUpdateView):
    model = models.Proposal
    form_class = forms.ProposalForm
    permission_required = 'meinberlin_kiezkasse.change_proposal'
    template_name = 'meinberlin_kiezkasse/proposal_update_form.html'


class ProposalDeleteView(module_views.ItemDeleteView):
    model = models.Proposal
    success_message = _("Your budget request has been deleted")
    permission_required = 'meinberlin_kiezkasse.change_proposal'
    template_name = 'meinberlin_kiezkasse/proposal_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ProposalDeleteView, self).delete(request, *args, **kwargs)


class ProposalModerateView(rules_mixins.PermissionRequiredMixin,
                           generic.UpdateView):
    model = models.Proposal
    form_class = forms.ProposalModerateForm
    permission_required = 'meinberlin_kiezkasse.moderate_proposal'
    template_name = 'meinberlin_kiezkasse/proposal_moderate_form.html'

    def get_success_url(self):
        return self.get_object().get_absolute_url()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['item'] = self.object
        kwargs['creator'] = self.request.user
        return kwargs
