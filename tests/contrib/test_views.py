import pytest

from tests.apps.questions.views import QuestionList


@pytest.mark.django_db
def test_sort_view_ordering_default(rf):
    request = rf.get(path='/')
    sort_view = QuestionList(request=request)
    sort_view.dispatch(request)
    assert sort_view.ordering == ['-created']


@pytest.mark.django_db
def test_sort_view_ordering_valid(rf):
    request = rf.get(path='/?ordering=text')
    sort_view = QuestionList(request=request)
    sort_view.dispatch(request)
    assert sort_view.ordering == ['text']


@pytest.mark.django_db
def test_sort_view_ordering_invalid(rf):
    request = rf.get(path='/?ordering=invalid')
    sort_view = QuestionList(request=request)
    sort_view.dispatch(request)
    assert sort_view.ordering == ['-created']


@pytest.mark.django_db
def test_sort_view_get_ordering(rf):
    request = rf.get(path='/?ordering=text')
    sort_view = QuestionList(request=request)
    sort_view.dispatch(request)
    assert sort_view.get_ordering() == 'text'


@pytest.mark.django_db
def test_sort_view_ordering_name(rf):
    request = rf.get(path='/')
    sort_view = QuestionList(request=request)
    sort_view.dispatch(request)
    assert sort_view.get_ordering_name() == 'Most recent'
