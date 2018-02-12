from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from adhocracy4.categories import filters as category_filters
from adhocracy4.filters import filters as a4_filters
from adhocracy4.filters import views as filter_views
from adhocracy4.filters import widgets as filters_widgets
from adhocracy4.filters.filters import FreeTextFilter
from adhocracy4.projects.mixins import ProjectMixin
from meinberlin.apps.contrib import filters
from meinberlin.apps.dashboard2 import mixins
from meinberlin.apps.ideas import views as idea_views

from . import forms
from . import models


class FreeTextFilterWidget(filters_widgets.FreeTextFilterWidget):
    label = _('Search')


class TopicFilterSet(a4_filters.DefaultsFilterSet):
    defaults = {
        'ordering': 'name'
    }
    category = category_filters.CategoryFilter()
    ordering = filters.OrderingFilter(
        choices=(
            ('name', _('Alphabetical')),
            ('-positive_rating_count', _('Most popular')),
            ('-comment_count', _('Most commented'))
        )
    )
    search = FreeTextFilter(
        widget=FreeTextFilterWidget,
        fields=['name']
    )

    class Meta:
        model = models.Topic
        fields = ['search', 'category']


class TopicListView(idea_views.AbstractIdeaListView):
    model = models.Topic
    filter_set = TopicFilterSet

    def get_queryset(self):
        return super().get_queryset()\
            .filter(module=self.module) \
            .annotate_positive_rating_count() \
            .annotate_negative_rating_count() \
            .annotate_comment_count()


class TopicDetailView(idea_views.AbstractIdeaDetailView):
    model = models.Topic
    queryset = models.Topic.objects.annotate_positive_rating_count()\
        .annotate_negative_rating_count()
    permission_required = 'meinberlin_topicprio.view_topic'


class TopicCreateFilterSet(a4_filters.DefaultsFilterSet):

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
        model = models.Topic
        fields = ['category']


class TopicListDashboardView(ProjectMixin,
                             mixins.DashboardBaseMixin,
                             mixins.DashboardComponentMixin,
                             filter_views.FilteredListView):
    model = models.Topic
    template_name = 'meinberlin_topicprio/topic_dashboard_list.html'
    filter_set = TopicCreateFilterSet
    permission_required = 'a4projects.change_project'

    def get_queryset(self):
        return super().get_queryset()\
            .filter(module=self.module) \
            .annotate_positive_rating_count() \
            .annotate_negative_rating_count() \
            .annotate_comment_count()

    def get_permission_object(self):
        return self.project


class TopicCreateView(mixins.DashboardBaseMixin,
                      mixins.DashboardComponentMixin,
                      mixins.DashboardComponentFormSignalMixin,
                      idea_views.AbstractIdeaCreateView):
    model = models.Topic
    form_class = forms.TopicForm
    permission_required = 'meinberlin_topicprio.add_topic'
    template_name = 'meinberlin_topicprio/topic_create_form.html'

    def get_success_url(self):
        return reverse(
            'a4dashboard:topic-list',
            kwargs={'module_slug': self.module.slug})

    def get_permission_object(self):
        return self.module


class TopicUpdateView(mixins.DashboardBaseMixin,
                      mixins.DashboardComponentMixin,
                      mixins.DashboardComponentFormSignalMixin,
                      idea_views.AbstractIdeaUpdateView):
    model = models.Topic
    form_class = forms.TopicForm
    permission_required = 'meinberlin_topicprio.change_topic'
    template_name = 'meinberlin_topicprio/topic_update_form.html'

    @property
    def organisation(self):
        return self.project.organisation

    def get_success_url(self):
        return reverse(
            'a4dashboard:topic-list',
            kwargs={'module_slug': self.module.slug})

    def get_permission_object(self):
        return self.get_object()


class TopicDeleteView(mixins.DashboardBaseMixin,
                      mixins.DashboardComponentMixin,
                      mixins.DashboardComponentDeleteSignalMixin,
                      idea_views.AbstractIdeaDeleteView):
    model = models.Topic
    success_message = _('The topic has been deleted')
    permission_required = 'meinberlin_topicprio.change_topic'
    template_name = 'meinberlin_topicprio/topic_confirm_delete.html'

    @property
    def organisation(self):
        return self.project.organisation

    def get_success_url(self):
        return reverse(
            'a4dashboard:topic-list',
            kwargs={'module_slug': self.module.slug})

    def get_permission_object(self):
        return self.get_object()
