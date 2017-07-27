from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from adhocracy4.filters import filters as a4_filters
from adhocracy4.filters import views as filter_views
from adhocracy4.modules import models as module_models
from adhocracy4.rules import mixins as rules_mixins
from meinberlin.apps.contrib import filters
from meinberlin.apps.contrib.views import ProjectContextDispatcher
from meinberlin.apps.exports import views as export_views

from . import forms
from . import models


def get_ordering_choices(request):
    choices = (('-created', _('Most recent')),)
    if request.project.last_active_module.has_feature('rate', models.Idea):
        choices += ('-positive_rating_count', _('Most popular')),
    choices += ('-comment_count', _('Most commented')),
    return choices


class IdeaFilterSet(a4_filters.DefaultsFilterSet):
    defaults = {
        'ordering': '-created'
    }
    category = filters.CategoryFilter()
    ordering = filters.OrderingFilter(
        choices=get_ordering_choices
    )

    class Meta:
        model = models.Idea
        fields = ['category']


class AbstractIdeaListView(ProjectContextDispatcher,
                           filter_views.FilteredListView):
    paginate_by = 15


class IdeaExportView(export_views.ItemExportView,
                     export_views.ItemExportWithRatesMixin,
                     export_views.ItemExportWithCommentCountMixin,
                     export_views.ItemExportWithCommentsMixin):
    model = models.Idea
    fields = ['name', 'description', 'creator', 'created']

    def get_queryset(self):
        return super().get_queryset() \
            .filter(module=self.module)\
            .annotate_comment_count()\
            .annotate_positive_rating_count()\
            .annotate_negative_rating_count()


class IdeaListView(AbstractIdeaListView):
    model = models.Idea
    filter_set = IdeaFilterSet
    exports = [(_('Ideas with comments'), IdeaExportView)]

    def get_queryset(self):
        return super().get_queryset()\
            .filter(module=self.project.last_active_module) \
            .annotate_positive_rating_count() \
            .annotate_negative_rating_count() \
            .annotate_comment_count()


class AbstractIdeaDetailView(ProjectContextDispatcher,
                             rules_mixins.PermissionRequiredMixin,
                             generic.DetailView):
    pass


class IdeaDetailView(AbstractIdeaDetailView):
    model = models.Idea
    queryset = models.Idea.objects.annotate_positive_rating_count()\
        .annotate_negative_rating_count()
    permission_required = 'meinberlin_ideas.view_idea'


class AbstractIdeaCreateView(ProjectContextDispatcher,
                             rules_mixins.PermissionRequiredMixin,
                             generic.CreateView):
    """Create an idea in the context of a module."""

    def dispatch(self, *args, **kwargs):
        mod_slug = self.kwargs[self.slug_url_kwarg]
        self.module = module_models.Module.objects.get(slug=mod_slug)
        kwargs['project'] = self.module.project
        return super().dispatch(*args, **kwargs)

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


class AbstractIdeaUpdateView(ProjectContextDispatcher,
                             rules_mixins.PermissionRequiredMixin,
                             generic.UpdateView):

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


class AbstractIdeaDeleteView(ProjectContextDispatcher,
                             rules_mixins.PermissionRequiredMixin,
                             generic.DeleteView):

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
