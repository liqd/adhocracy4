import django_filters

from adhocracy4.contrib.views import FilteredListView

from . import models


class QuestionFilterSet(django_filters.FilterSet):

    class Meta:
        model = models.Question
        fields = ['text']


class QuestionList(FilteredListView):
    model = models.Question
    filter_set = QuestionFilterSet
