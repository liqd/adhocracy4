from unittest import mock

import pytest
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.http import HttpResponseServerError
from django.views.generic import View
from freezegun import freeze_time

from adhocracy4.projects import models, views


def dispatch_view(view_class, request, *args, **kwargs):
    """Mimic as_view() and dispatch() but returns view instance in addition."""
    view = view_class()
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view.dispatch(request, *args, **kwargs), view


def project_detail_view_factory(_project):
    class FakeProjectDetailView(views.PhaseDispatcher, View):
        model = models.Project
        project = _project

        def get(self, request, *args, **kwargs):
            return HttpResponse('project_detail')
    return FakeProjectDetailView.as_view()


@pytest.mark.django_db
def test_phase_dispatcher_phase(rf, phase):
    project = phase.module.project
    view = project_detail_view_factory(project)

    with freeze_time(phase.start_date):
        request = rf.get('/url')
        response = view(request)
        assert 'a4test_questions/question_list.html' in response.template_name

    with freeze_time(phase.end_date):
        request = rf.get('/url')
        response = view(request)
        assert 'a4test_questions/question_list.html' in response.template_name


@pytest.mark.django_db
def test_phase_dispatcher_default(rf, project):
    view = project_detail_view_factory(project)
    request = rf.get('/url')
    response = view(request)
    assert response.content == b'project_detail'


class FakeProjectContextView(views.ProjectContextDispatcher):
    def get(self, request, *args, **kwargs):
        return HttpResponse('project_context')


@pytest.mark.django_db
def test_project_context_kwargs(rf, project):
    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextView,
                                   request, project=project)

    assert response.content == b'project_context'
    assert view.project == project
    assert request.project == project


@pytest.mark.django_db
def test_project_context_url(rf, project):
    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextView,
                                   request,
                                   project_slug=project.slug)

    assert response.content == b'project_context'
    assert view.project == project
    assert request.project == project


@pytest.mark.django_db
def test_project_context_url_overwrite(rf, project):
    class FakeProjectContextViewUrlOverwrite(FakeProjectContextView):
        project_lookup_field = 'id'
        project_url_kwarg = 'project_id'

    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextViewUrlOverwrite,
                                   request,
                                   project_id=project.id)

    assert response.content == b'project_context'
    assert view.project == project
    assert request.project == project


@pytest.mark.django_db
def test_project_context_object(rf, project):
    class FakeProjectContextGetObjectView(FakeProjectContextView):
        def get_object(self):
            return mock.Mock(project=project)

    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextGetObjectView,
                                   request)

    assert response.content == b'project_context'
    assert view.project == project
    assert request.project == project


@pytest.mark.django_db
def test_project_context_project_object(rf, project):
    class FakeProjectContextGetObjectView(FakeProjectContextView):
        def get_object(self):
            return project

    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextGetObjectView,
                                   request)

    assert response.content == b'project_context'
    assert view.project == project
    assert request.project == project


@pytest.mark.django_db
def test_project_context_overwrite(rf, project):
    class FakeProjectContextGetProjectView(FakeProjectContextView):
        def get_project(self, *args, **kwargs):
            return project

    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextGetProjectView,
                                   request)

    assert response.content == b'project_context'
    assert view.project == project
    assert request.project == project


@pytest.mark.django_db
def test_project_context_missing(rf):
    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextView,
                                   request)

    assert response.status_code == HttpResponseServerError.status_code


@pytest.mark.django_db
def test_project_context_invalid(rf, project_factory):
    class FakeProjectContextViewInvalid(FakeProjectContextView):
        def get_project(self, *args, **kwargs):
            return project_factory()

        def get_object(self):
            return mock.Mock(project=project_factory())

    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextViewInvalid,
                                   request)

    assert response.status_code == HttpResponseForbidden.status_code


@pytest.mark.django_db
def test_project_template_context(rf, project):
    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextView,
                                   request, project=project)

    context = view.get_context_data()
    assert context['project'] == project
