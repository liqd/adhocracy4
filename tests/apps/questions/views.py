import django_filters

from adhocracy4.modules import views as module_views

from . import models


class QuestionFilterSet(django_filters.FilterSet):

    class Meta:
        model = models.Question
        fields = ['text']


class QuestionList(module_views.ItemListView):
    model = models.Question
    filter_set = QuestionFilterSet
