from django.core.urlresolvers import reverse
from django.views import generic

from adhocracy4.filters import views as filter_views
from adhocracy4.projects import mixins as project_mixins
from adhocracy4.rules import mixins as rules_mixins

from . import models


class ItemListView(project_mixins.ProjectMixin, filter_views.FilteredListView):
    model = None
    paginate_by = 15
    filter_set = None


class ItemDetailView(rules_mixins.PermissionRequiredMixin, generic.DetailView):
    model = None
    permission_required = None


class ItemCreateView(rules_mixins.PermissionRequiredMixin, generic.CreateView):
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
        return kwargs


class ItemUpdateView(rules_mixins.PermissionRequiredMixin, generic.UpdateView):
    model = None
    form_class = None
    permission_required = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['module'] = self.object.module
        return kwargs


class ItemDeleteView(rules_mixins.PermissionRequiredMixin, generic.DeleteView):
    model = None
    permission_required = None

    def get_success_url(self):
        return reverse(
            'project-detail', kwargs={'slug': self.object.project.slug})
