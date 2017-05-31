from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from adhocracy4.filters import filters as a4_filters
from adhocracy4.filters import views as filter_views
from adhocracy4.modules import views as module_views
from adhocracy4.rules import mixins as rules_mixins

from apps.contrib import filters
from apps.dashboard.mixins import DashboardBaseMixin

from . import forms
from . import models


class TopicFilterSet(a4_filters.DefaultsFilterSet):

    defaults = {
        'ordering': '-positive_rating_count'
    }

    category = filters.CategoryFilter()

    ordering = filters.OrderingFilter(
        choices=(
            ('-positive_rating_count', _('Most popular')),
            ('-comment_count', _('Most commented'))
        )
    )

    class Meta:
        model = models.Topic
        fields = ['category']


class TopicListView(module_views.ItemListView):
    model = models.Topic
    filter_set = TopicFilterSet

    def get_queryset(self):
        return super().get_queryset().filter(module=self.module) \
            .annotate_positive_rating_count() \
            .annotate_negative_rating_count() \
            .annotate_comment_count()


class TopicDetailView(module_views.ItemDetailView):
    model = models.Topic
    queryset = models.Topic.objects.annotate_positive_rating_count()\
        .annotate_negative_rating_count()
    permission_required = 'meinberlin_topicprio.view_topic'


class TopicCreateFilterSet(a4_filters.PagedFilterSet):

    category = filters.CategoryFilter()

    class Meta:
        model = models.Topic
        fields = ['category']


class TopicMgmtView(DashboardBaseMixin,
                    rules_mixins.PermissionRequiredMixin,
                    filter_views.FilteredListView):
    model = models.Topic
    template_name = 'meinberlin_topicprio/topic_mgmt_list.html'
    filter_set = TopicCreateFilterSet
    permission_required = 'a4projects.add_project'

    # Dashboard related attributes
    menu_item = 'project'

    def get_success_url(self):
        return reverse(
            'dashboard-project-list',
            kwargs={'organisation_slug': self.organisation.slug, })

    def dispatch(self, *args, **kwargs):
        self.project = kwargs['project']
        self.module = self.project.module_set.first()
        self.request.module = self.module
        return super(TopicMgmtView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(module=self.module) \
            .annotate_positive_rating_count() \
            .annotate_negative_rating_count() \
            .annotate_comment_count()


class TopicMgmtCreateView(module_views.ItemCreateView):
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


class TopicMgmtUpdateView(module_views.ItemUpdateView):
    model = models.Topic
    form_class = forms.TopicForm
    permission_required = 'meinberlin_topicprio.change_topic'
    template_name = 'meinberlin_topicprio/topic_mgmt_update_form.html'
    menu_item = 'project'

    @property
    def organisation(self):
        return self.get_object().project.organisation

    def get_success_url(self):
        return reverse(
            'dashboard-project-management',
            kwargs={'slug': self.get_object().project.slug})


class TopicMgmtDeleteView(module_views.ItemDeleteView):
    model = models.Topic
    success_message = _('The topic has been deleted')
    permission_required = 'meinberlin_topicprio.change_topic'
    template_name = 'meinberlin_topicprio/topic_mgmt_confirm_delete.html'
    menu_item = 'project'

    @property
    def organisation(self):
        return self.get_object().project.organisation

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'dashboard-project-management',
            kwargs={'slug': self.get_object().project.slug})
