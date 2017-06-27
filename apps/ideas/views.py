from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from adhocracy4.filters import filters as a4_filters
from adhocracy4.filters import views as filter_views
from adhocracy4.projects import views as project_views
from adhocracy4.rules import mixins as rules_mixins
from apps.contrib import filters

from . import forms
from . import models


def get_ordering_choices(request):
    choices = (('-created', _('Most recent')),)
    if request.module.has_feature('rate', models.Idea):
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


class AbstractIdeaListView(project_views.ProjectContextDispatcher,
                           filter_views.FilteredListView):
    model = None
    paginate_by = 15
    filter_set = None


class IdeaListView(AbstractIdeaListView):
    model = models.Idea
    filter_set = IdeaFilterSet

    def get_queryset(self):
        return super().get_queryset()\
            .filter(module=self.project.active_module) \
            .annotate_positive_rating_count() \
            .annotate_negative_rating_count() \
            .annotate_comment_count()


class AbstractIdeaDetailView(project_views.ProjectContextDispatcher,
                             rules_mixins.PermissionRequiredMixin,
                             generic.DetailView):
    model = None
    permission_required = None


class IdeaDetailView(AbstractIdeaDetailView):
    model = models.Idea
    queryset = models.Idea.objects.annotate_positive_rating_count()\
        .annotate_negative_rating_count()
    permission_required = 'meinberlin_ideas.view_idea'


class AbstractIdeaCreateView(project_views.ProjectContextDispatcher,
                             rules_mixins.PermissionRequiredMixin,
                             generic.CreateView):
    model = None
    form_class = None
    permission_required = None

    def dispatch(self, *args, **kwargs):
        mod_slug = self.kwargs[self.slug_url_kwarg]
        self.module = models.Module.objects.get(slug=mod_slug)
        self.project = self.module.project
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


class AbstractIdeaUpdateView(project_views.ProjectContextDispatcher,
                             rules_mixins.PermissionRequiredMixin,
                             generic.UpdateView):
    model = None
    form_class = None
    permission_required = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['module'] = self.object.module
        if self.object.module.settings_instance:
            kwargs['settings_instance'] = self.object.module.settings_instance
        return kwargs


class IdeaUpdateView(AbstractIdeaUpdateView):
    model = models.Idea
    form_class = forms.IdeaForm
    permission_required = 'meinberlin_ideas.change_idea'
    template_name = 'meinberlin_ideas/idea_update_form.html'


class AbstractIdeaDeleteView(project_views.ProjectContextDispatcher,
                             rules_mixins.PermissionRequiredMixin,
                             generic.DeleteView):
    model = None
    permission_required = None

    def get_success_url(self):
        return reverse(
            'project-detail', kwargs={'slug': self.object.project.slug})


class IdeaDeleteView(AbstractIdeaDeleteView):
    model = models.Idea
    success_message = _('Your Idea has been deleted')
    permission_required = 'meinberlin_ideas.change_idea'
    template_name = 'meinberlin_ideas/idea_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(IdeaDeleteView, self).delete(request, *args, **kwargs)
