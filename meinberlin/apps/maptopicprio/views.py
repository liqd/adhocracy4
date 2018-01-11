from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from adhocracy4.categories import filters as category_filters
from adhocracy4.filters import filters as a4_filters
from adhocracy4.filters import views as filter_views
from adhocracy4.projects.mixins import ProjectMixin
from meinberlin.apps.contrib import filters
from meinberlin.apps.dashboard2 import mixins
from meinberlin.apps.ideas import views as idea_views

from . import forms
from . import models


def get_ordering_choices(view):
    choices = (('-created', _('Most recent')),)
    if view.module.has_feature('rate', models.MapTopic):
        choices += ('-positive_rating_count', _('Most popular')),
    choices += ('-comment_count', _('Most commented')),
    return choices


class MapTopicFilterSet(a4_filters.DefaultsFilterSet):
    defaults = {
        'ordering': '-created'
    }
    category = category_filters.CategoryFilter()
    ordering = filters.OrderingFilter(
        choices=get_ordering_choices
    )

    class Meta:
        model = models.MapTopic
        fields = ['category']


class MapTopicCreateFilterSet(a4_filters.DefaultsFilterSet):

    defaults = {
        'ordering': 'name'
    }

    category = category_filters.CategoryFilter()

    ordering = filters.OrderingFilter(
        choices=(
            ('name', _('Alphabetical')),
        )
    )

    class Meta:
        model = models.MapTopic
        fields = ['category']


class MapTopicDetailView(idea_views.AbstractIdeaDetailView):
    model = models.MapTopic
    queryset = models.MapTopic.objects.annotate_positive_rating_count()\
        .annotate_negative_rating_count()
    permission_required = 'meinberlin_maptopicprio.view_maptopic'


class MapTopicListView(idea_views.AbstractIdeaListView):
    model = models.MapTopic
    filter_set = MapTopicFilterSet

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


class MapTopicListDashboardView(ProjectMixin,
                                mixins.DashboardBaseMixin,
                                mixins.DashboardComponentMixin,
                                filter_views.FilteredListView):
    model = models.MapTopic
    template_name = 'meinberlin_maptopicprio/maptopic_dashboard_list.html'
    filter_set = MapTopicCreateFilterSet
    permission_required = 'a4projects.change_project'

    def get_queryset(self):
        return super().get_queryset()\
            .filter(module=self.module) \
            .annotate_positive_rating_count() \
            .annotate_negative_rating_count() \
            .annotate_comment_count()

    def get_permission_object(self):
        return self.project


class MapTopicCreateView(mixins.DashboardBaseMixin,
                         mixins.DashboardComponentMixin,
                         mixins.DashboardComponentFormSignalMixin,
                         idea_views.AbstractIdeaCreateView):
    model = models.MapTopic
    form_class = forms.MapTopicForm
    permission_required = 'meinberlin_maptopicprio.add_maptopic'
    template_name = 'meinberlin_maptopicprio/maptopic_create_form.html'

    def get_success_url(self):
        return reverse(
            'a4dashboard:maptopic-list',
            kwargs={'module_slug': self.module.slug})

    def get_permission_object(self):
        return self.module


class MapTopicUpdateView(mixins.DashboardBaseMixin,
                         mixins.DashboardComponentMixin,
                         mixins.DashboardComponentFormSignalMixin,
                         idea_views.AbstractIdeaUpdateView):
    model = models.MapTopic
    form_class = forms.MapTopicForm
    permission_required = 'meinberlin_maptopicprio.change_maptopic'
    template_name = 'meinberlin_maptopicprio/maptopic_update_form.html'

    @property
    def organisation(self):
        return self.project.organisation

    def get_success_url(self):
        return reverse(
            'a4dashboard:maptopic-list',
            kwargs={'module_slug': self.module.slug})

    def get_permission_object(self):
        return self.get_object()


class MapTopicDeleteView(mixins.DashboardBaseMixin,
                         mixins.DashboardComponentMixin,
                         mixins.DashboardComponentDeleteSignalMixin,
                         idea_views.AbstractIdeaDeleteView):
    model = models.MapTopic
    success_message = _('The place has been deleted')
    permission_required = 'meinberlin_maptopicprio.change_maptopic'
    template_name = 'meinberlin_maptopicprio/maptopic_confirm_delete.html'

    @property
    def organisation(self):
        return self.project.organisation

    def get_success_url(self):
        return reverse(
            'a4dashboard:maptopic-list',
            kwargs={'module_slug': self.module.slug})

    def get_permission_object(self):
        return self.get_object()
