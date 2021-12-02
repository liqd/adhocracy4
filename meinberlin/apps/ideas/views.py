from django.contrib import messages
from django.db import transaction
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import generic

from adhocracy4.categories import filters as category_filters
from adhocracy4.exports.views import DashboardExportView
from adhocracy4.filters import filters as a4_filters
from adhocracy4.filters import views as filter_views
from adhocracy4.filters import widgets as filters_widgets
from adhocracy4.filters.filters import FreeTextFilter
from adhocracy4.projects.mixins import DisplayProjectOrModuleMixin
from adhocracy4.projects.mixins import ProjectMixin
from adhocracy4.rules import mixins as rules_mixins
from meinberlin.apps.contrib import forms as contrib_forms
from meinberlin.apps.contrib.views import CanonicalURLDetailView
from meinberlin.apps.moderatorfeedback.forms import ModeratorStatementForm
from meinberlin.apps.moderatorfeedback.models import ModeratorStatement
from meinberlin.apps.notifications.emails import \
    NotifyCreatorOnModeratorFeedback

from . import forms
from . import models


class FreeTextFilterWidget(filters_widgets.FreeTextFilterWidget):
    label = _('Search')


def get_ordering_choices(view):
    choices = (('-created', _('Most recent')),)
    if view.module.has_feature('rate', models.Idea):
        choices += ('-positive_rating_count', _('Most popular')),
    choices += ('-comment_count', _('Most commented')),
    return choices


class IdeaFilterSet(a4_filters.DefaultsFilterSet):
    defaults = {
        'ordering': '-created'
    }
    category = category_filters.CategoryFilter()
    ordering = a4_filters.DynamicChoicesOrderingFilter(
        choices=get_ordering_choices
    )
    search = FreeTextFilter(
        widget=FreeTextFilterWidget,
        fields=['name']
    )

    class Meta:
        model = models.Idea
        fields = ['search', 'category']


class AbstractIdeaListView(ProjectMixin,
                           filter_views.FilteredListView):
    paginate_by = 15


class IdeaListView(AbstractIdeaListView,
                   DisplayProjectOrModuleMixin
                   ):
    model = models.Idea
    filter_set = IdeaFilterSet

    def get_queryset(self):
        return super().get_queryset()\
            .filter(module=self.module)


class AbstractIdeaDetailView(ProjectMixin,
                             rules_mixins.PermissionRequiredMixin,
                             CanonicalURLDetailView):
    get_context_from_object = True


class IdeaDetailView(AbstractIdeaDetailView):
    model = models.Idea
    queryset = models.Idea.objects.annotate_positive_rating_count()\
        .annotate_negative_rating_count()
    permission_required = 'meinberlin_ideas.view_idea'


class AbstractIdeaCreateView(ProjectMixin,
                             rules_mixins.PermissionRequiredMixin,
                             generic.CreateView):
    """Create an idea in the context of a module."""

    def get_permission_object(self, *args, **kwargs):
        return self.module

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.module = self.module
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['module'] = self.module
        if self.module.settings_instance:
            kwargs['settings_instance'] = self.module.settings_instance
        return kwargs


class IdeaCreateView(AbstractIdeaCreateView):
    model = models.Idea
    form_class = forms.IdeaForm
    permission_required = 'meinberlin_ideas.add_idea'
    template_name = 'meinberlin_ideas/idea_create_form.html'


class AbstractIdeaUpdateView(ProjectMixin,
                             rules_mixins.PermissionRequiredMixin,
                             generic.UpdateView):
    get_context_from_object = True

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        instance = kwargs.get('instance')
        kwargs['module'] = instance.module
        if instance.module.settings_instance:
            kwargs['settings_instance'] = \
                instance.module.settings_instance
        return kwargs


class IdeaUpdateView(AbstractIdeaUpdateView):
    model = models.Idea
    form_class = forms.IdeaForm
    permission_required = 'meinberlin_ideas.change_idea'
    template_name = 'meinberlin_ideas/idea_update_form.html'


class AbstractIdeaDeleteView(ProjectMixin,
                             rules_mixins.PermissionRequiredMixin,
                             generic.DeleteView):
    get_context_from_object = True

    def get_success_url(self):
        return reverse(
            'project-detail', kwargs={'slug': self.project.slug})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(AbstractIdeaDeleteView, self)\
            .delete(request, *args, **kwargs)


class IdeaDeleteView(AbstractIdeaDeleteView):
    model = models.Idea
    success_message = _('Your Idea has been deleted')
    permission_required = 'meinberlin_ideas.change_idea'
    template_name = 'meinberlin_ideas/idea_confirm_delete.html'


class AbstractIdeaModerateView(
        ProjectMixin,
        rules_mixins.PermissionRequiredMixin,
        generic.detail.SingleObjectMixin,
        generic.detail.SingleObjectTemplateResponseMixin,
        contrib_forms.BaseMultiModelFormView):

    get_context_from_object = True

    def __init__(self):
        self.forms = {
            'moderateable': {
                'model': self.model,
                'form_class': self.moderateable_form_class
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
        moderateable = objects['moderateable']
        statement = objects['statement']

        if not statement.pk:
            statement.creator = self.request.user

        with transaction.atomic():
            statement.save()
            moderateable.moderator_statement = statement
            moderateable.save()
            NotifyCreatorOnModeratorFeedback.send(self.object)
        return objects

    def get_instance(self, name):
        if name == 'moderateable':
            return self.object
        elif name == 'statement':
            return self.object.moderator_statement


class IdeaModerateView(AbstractIdeaModerateView):
    model = models.Idea
    permission_required = 'meinberlin_ideas.moderate_idea'
    template_name = 'meinberlin_ideas/idea_moderate_form.html'
    moderateable_form_class = forms.IdeaModerateForm


class IdeaDashboardExportView(DashboardExportView):
    template_name = 'a4exports/export_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['export'] = reverse(
            'a4dashboard:idea-export',
            kwargs={'module_slug': self.module.slug})
        context['comment_export'] = reverse(
            'a4dashboard:idea-comment-export',
            kwargs={'module_slug': self.module.slug})
        return context
