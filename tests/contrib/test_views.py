import pytest

from tests.apps.questions.views import QuestionList


@pytest.mark.django_db
def test_sort_view_ordering_default(request_factory):
    request = request_factory.get(path='/')
    sort_view = QuestionList(request=request)
    sort_view.dispatch(request)
    assert sort_view.ordering == ['-created']


@pytest.mark.django_db
def test_sort_view_ordering_valid(request_factory):
    request = request_factory.get(path='/?ordering=text')
    sort_view = QuestionList(request=request)
    sort_view.dispatch(request)
    assert sort_view.ordering == ['text']


@pytest.mark.django_db
def test_sort_view_ordering_invalid(request_factory):
    request = request_factory.get(path='/?ordering=invalid')
    sort_view = QuestionList(request=request)
    sort_view.dispatch(request)
    assert sort_view.ordering == ['-created']


@pytest.mark.django_db
def test_sort_view_get_ordering(request_factory):
    request = request_factory.get(path='/?ordering=text')
    sort_view = QuestionList(request=request)
    sort_view.dispatch(request)
    assert sort_view.get_ordering() == 'text'


@pytest.mark.django_db
def test_sort_view_ordering_name(request_factory):
    request = request_factory.get(path='/')
    sort_view = QuestionList(request=request)
    sort_view.dispatch(request)
    assert sort_view.get_ordering_name() == 'Most recent'
