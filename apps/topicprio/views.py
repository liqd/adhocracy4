import django_filters
from django.contrib import messages
from django.utils.translation import ugettext as _

from adhocracy4.modules import views as module_views

from apps.contrib import filters

from . import forms
from . import models


class TopicCreateFilterSet(django_filters.FilterSet):

    category = filters.CategoryFilter()

    class Meta:
        model = models.Topic
        fields = ['category']


class TopicCreateListView(module_views.ItemListView):
    model = models.Topic
    filter_set = TopicCreateFilterSet
    template_name = 'meinberlin_topicprio/topic_create_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(module=self.module) \
            .annotate_positive_rating_count() \
            .annotate_negative_rating_count() \
            .annotate_comment_count()


class TopicFilterSet(TopicCreateFilterSet):

    ordering = filters.OrderingFilter(
        choices=(
            ('-created', _('Most recent')),
            ('-positive_rating_count', _('Most popular')),
            ('-comment_count', _('Most commented'))
        )
    )


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


class TopicCreateView(module_views.ItemCreateView):
    model = models.Topic
    form_class = forms.TopicForm
    permission_required = 'meinberlin_topicprio.create_topic'
    template_name = 'meinberlin_topicprio/topic_create_form.html'


class TopicUpdateView(module_views.ItemUpdateView):
    model = models.Topic
    form_class = forms.TopicForm
    permission_required = 'meinberlin_topicprio.change_topic'
    template_name = 'meinberlin_topicprio/topic_update_form.html'


class TopicDeleteView(module_views.ItemDeleteView):
    model = models.Topic
    success_message = _("The topic has been deleted")
    permission_required = 'meinberlin_topicprio.change_topic'
    template_name = 'meinberlin_topicprio/topic_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
