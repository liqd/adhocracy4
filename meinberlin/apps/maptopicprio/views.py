from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from adhocracy4.filters import filters as a4_filters
from adhocracy4.filters import views as filter_views
from meinberlin.apps.contrib import filters
from meinberlin.apps.dashboard2 import mixins
from meinberlin.apps.exports import views as export_views
from meinberlin.apps.ideas import views as idea_views

from . import forms
from . import models


def get_ordering_choices(request):
    choices = (('-created', _('Most recent')),)
    if request.module.has_feature('rate', models.MapTopic):
        choices += ('-positive_rating_count', _('Most popular')),
    choices += ('-comment_count', _('Most commented')),
    return choices


class MapTopicFilterSet(a4_filters.DefaultsFilterSet):
    defaults = {
        'ordering': '-created'
    }
    category = filters.CategoryFilter()
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

    category = filters.CategoryFilter()

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
    permission_required = 'meinberlin_topicprio.view_topic'


class MapTopicExportView(export_views.ItemExportView,
                         export_views.ItemExportWithRatesMixin,
                         export_views.ItemExportWithCommentCountMixin,
                         export_views.ItemExportWithCommentsMixin,
                         export_views.ItemExportWithLocationMixin):
    model = models.MapTopic
    fields = ['name', 'description', 'creator', 'created']

    def get_queryset(self):
        return super().get_queryset() \
            .filter(module=self.module)\
            .annotate_comment_count()\
            .annotate_positive_rating_count()\
            .annotate_negative_rating_count()


class MapTopicListView(idea_views.AbstractIdeaListView):
    model = models.MapTopic
    filter_set = MapTopicFilterSet
    exports = [(_('Topics with comments'), MapTopicExportView)]

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


class MapTopicListDashboardView(mixins.DashboardComponentMixin,
                                mixins.DashboardBaseMixin,
                                mixins.DashboardContextMixin,
                                filter_views.FilteredListView):
    model = models.MapTopic
    template_name = 'meinberlin_maptopicprio/maptopic_dashboard_list.html'
    filter_set = MapTopicCreateFilterSet
    permission_required = 'a4projects.add_project'
    module_url_kwarg = 'module_slug'

    def get_queryset(self):
        return super().get_queryset()\
            .filter(module=self.module) \
            .annotate_positive_rating_count() \
            .annotate_negative_rating_count() \
            .annotate_comment_count()


class MapTopicCreateView(mixins.DashboardComponentMixin,
                         mixins.DashboardBaseMixin,
                         mixins.DashboardContextMixin,
                         idea_views.AbstractIdeaCreateView):
    model = models.MapTopic
    form_class = forms.MapTopicForm
    permission_required = 'meinberlin_topicprio.add_topic'
    template_name = 'meinberlin_maptopicprio/maptopic_create_form.html'
    module_url_kwarg = 'module_slug'

    def get_success_url(self):
        return reverse(
            'a4dashboard:maptopic-list',
            kwargs={'module_slug': self.module.slug})


class MapTopicUpdateView(mixins.DashboardComponentMixin,
                         mixins.DashboardBaseMixin,
                         mixins.DashboardContextMixin,
                         idea_views.AbstractIdeaUpdateView):
    model = models.MapTopic
    form_class = forms.MapTopicForm
    permission_required = 'meinberlin_topicprio.change_topic'
    template_name = 'meinberlin_maptopicprio/maptopic_update_form.html'

    @property
    def organisation(self):
        return self.project.organisation

    def get_success_url(self):
        return reverse(
            'a4dashboard:maptopic-list',
            kwargs={'module_slug': self.module.slug})


class MapTopicDeleteView(mixins.DashboardComponentMixin,
                         mixins.DashboardBaseMixin,
                         mixins.DashboardContextMixin,
                         idea_views.AbstractIdeaDeleteView):
    model = models.MapTopic
    success_message = _('The topic has been deleted')
    permission_required = 'meinberlin_topicprio.change_topic'
    template_name = 'meinberlin_maptopicprio/maptopic_confirm_delete.html'

    @property
    def organisation(self):
        return self.project.organisation

    def get_success_url(self):
        return reverse(
            'a4dashboard:maptopic-list',
            kwargs={'module_slug': self.module.slug})
