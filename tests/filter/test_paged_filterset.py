from adhocracy4.filters.filters import PagedFilterSet
from tests.apps.questions import models as question_models


class TextFilterSet(PagedFilterSet):

    class Meta:
        model = question_models.Question
        fields = ['text']


def test_page_clean_query(rf):
    request = rf.get('/questions', {
        'page': 1
    })

    filterset = TextFilterSet(data=request.GET, request=request, view=None)
    assert 'page' not in filterset.data
