from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from adhocracy4.filters import filters as a4_filters
from adhocracy4.filters import views as filter_views
from adhocracy4.rules import mixins as rules_mixins
from meinberlin.apps.contrib import filters
from meinberlin.apps.contrib.views import ProjectContextDispatcher
from meinberlin.apps.dashboard.mixins import DashboardBaseMixin
from meinberlin.apps.exports import views as export_views
from meinberlin.apps.ideas import views as idea_views

from . import forms
from . import models


class TopicFilterSet(a4_filters.DefaultsFilterSet):
    defaults = {
        'ordering': 'name'
    }
    category = filters.CategoryFilter()
    ordering = filters.OrderingFilter(
        choices=(
            ('name', _('Alphabetical')),
            ('-positive_rating_count', _('Most popular')),
            ('-comment_count', _('Most commented'))
        )
    )

    class Meta:
        model = models.Topic
        fields = ['category']


class TopicExportView(export_views.ItemExportView,
                      export_views.ItemExportWithRatesMixin,
                      export_views.ItemExportWithCommentCountMixin,
                      export_views.ItemExportWithCommentsMixin):
    model = models.Topic
    fields = ['name', 'description', 'creator', 'created']

    def get_queryset(self):
        return super().get_queryset() \
            .filter(module=self.module)\
            .annotate_comment_count()\
            .annotate_positive_rating_count()\
            .annotate_negative_rating_count()


class TopicListView(idea_views.AbstractIdeaListView):
    model = models.Topic
    filter_set = TopicFilterSet
    exports = [(_('Topics with comments'), TopicExportView)]

    def get_queryset(self):
        return super().get_queryset()\
            .filter(module=self.project.last_active_module) \
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

    category = filters.CategoryFilter()

    ordering = filters.OrderingFilter(
        choices=(
            ('name', _('Alphabetical')),
        )
    )

    class Meta:
        model = models.Topic
        fields = ['category']


class TopicMgmtView(ProjectContextDispatcher,
                    DashboardBaseMixin,
                    rules_mixins.PermissionRequiredMixin,
                    filter_views.FilteredListView):
    model = models.Topic
    template_name = 'meinberlin_topicprio/topic_mgmt_list.html'
    filter_set = TopicCreateFilterSet
    permission_required = 'a4projects.add_project'
    project_url_kwarg = 'slug'

    # Dashboard related attributes
    menu_item = 'project'

    def get_success_url(self):
        return reverse(
            'dashboard-project-list',
            kwargs={'organisation_slug': self.organisation.slug, })

    def get_queryset(self):
        # FIXME: Add multi-module support
        module = self.project.module_set.first()
        return super().get_queryset()\
            .filter(module=module) \
            .annotate_positive_rating_count() \
            .annotate_negative_rating_count() \
            .annotate_comment_count()


class TopicMgmtCreateView(idea_views.AbstractIdeaCreateView):
    model = models.Topic
    form_class = forms.TopicForm
    permission_required = 'meinberlin_topicprio.add_topic'
    template_name = 'meinberlin_topicprio/topic_mgmt_create_form.html'
    menu_item = 'project'

    @property
    def organisation(self):
        return self.project.organisation

    def get_success_url(self):
        return reverse(
            'dashboard-project-management',
            kwargs={'slug': self.project.slug})


class TopicMgmtUpdateView(idea_views.AbstractIdeaUpdateView):
    model = models.Topic
    form_class = forms.TopicForm
    permission_required = 'meinberlin_topicprio.change_topic'
    template_name = 'meinberlin_topicprio/topic_mgmt_update_form.html'
    menu_item = 'project'

    @property
    def organisation(self):
        return self.project.organisation

    def get_success_url(self):
        return reverse(
            'dashboard-project-management',
            kwargs={'slug': self.project.slug})


class TopicMgmtDeleteView(idea_views.AbstractIdeaDeleteView):
    model = models.Topic
    success_message = _('The topic has been deleted')
    permission_required = 'meinberlin_topicprio.change_topic'
    template_name = 'meinberlin_topicprio/topic_mgmt_confirm_delete.html'
    menu_item = 'project'

    @property
    def organisation(self):
        return self.project.organisation

    def get_success_url(self):
        return reverse(
            'dashboard-project-management',
            kwargs={'slug': self.project.slug})
