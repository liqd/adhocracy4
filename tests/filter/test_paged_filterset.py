from tests.apps.questions import models as question_models

from adhocracy4.filters.filters import PagedFilterSet


class TextFilter(PagedFilterSet):

    class Meta:
        model = question_models.Question
        fields = ['text']


def test_page_clean_query(rf):
    request = rf.get('/questions', {
        'page': 1
    })

    filterset = TextFilter(data=request.GET, request=request)
    assert 'page' not in filterset.data
