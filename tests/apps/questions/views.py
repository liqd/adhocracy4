import django_filters

from adhocracy4.filters import views as filter_views
from adhocracy4.projects import views as project_views
from . import models


class QuestionFilterSet(django_filters.FilterSet):

    class Meta:
        model = models.Question
        fields = ['text']


class QuestionList(project_views.ProjectContextDispatcher,
                   filter_views.FilteredListView):
    model = models.Question
    filter_set = QuestionFilterSet
