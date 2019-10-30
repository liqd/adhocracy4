from unittest import mock

import pytest
from dateutil.parser import parse
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic import View
from freezegun import freeze_time

from adhocracy4.projects import mixins
from adhocracy4.projects import models
from adhocracy4.test.helpers import dispatch_view
from tests.apps.questions import models as question_models


class FakeProjectContextView(mixins.ProjectMixin, View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('project_context')


@pytest.fixture
def project_detail_view():
    class FakeProjectDetailView(mixins.PhaseDispatchMixin, View):
        model = models.Project

        def get(self, request, *args, **kwargs):
            return HttpResponse('project_detail')
    return FakeProjectDetailView.as_view()


@pytest.fixture
def question_list_view():
    class DummyView(mixins.ProjectMixin, ListView):
        model = question_models.Question
    return DummyView.as_view()


@pytest.mark.django_db
def test_phase_dispatch_mixin_phase(rf, project_detail_view, phase):
    project = phase.module.project

    with freeze_time(phase.start_date):
        request = rf.get('/url')
        response = project_detail_view(request, slug=project.slug)
        assert 'a4test_questions/question_list.html' in response.template_name

    with freeze_time(phase.end_date):
        request = rf.get('/url')
        response = project_detail_view(request, slug=project.slug)
        assert 'a4test_questions/question_list.html' in response.template_name


@pytest.mark.django_db
def test_phase_dispatch_mixin_default(rf, project_detail_view, project):
    request = rf.get('/url')
    response = project_detail_view(request, slug=project.slug)
    assert response.content == b'project_detail'


@pytest.mark.django_db
def test_project_inject_phase_after_finish(rf, phase_factory,
                                           question_list_view):
    phase = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )
    module = phase.module
    project = module.project

    request = rf.get('/project_name/ideas')

    with freeze_time(phase.end_date):
        response = question_list_view(request, project=project, module=module)

    response = question_list_view(request, project=project, module=module)
    view_data = response.context_data['view']
    assert view_data.project == project
    assert view_data.module == module


@pytest.mark.django_db
def test_project_mixin_kwargs(rf, project):
    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextView, request,
                                   project=project)
    assert view.project == project


@pytest.mark.django_db
def test_project_mixin_url(rf, project):
    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextView, request,
                                   project_slug=project.slug)
    assert view.project == project


@pytest.mark.django_db
def test_project_mixin_url_overwrite(rf, project):
    class FakeProjectContextViewUrlOverwrite(FakeProjectContextView):
        project_lookup_field = 'id'
        project_url_kwarg = 'project_id'

    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextViewUrlOverwrite, request,
                                   project_id=project.id)
    assert view.project == project


@pytest.mark.django_db
def test_project_mixin_object(rf, project):
    class FakeProjectContextGetObjectView(FakeProjectContextView):
        get_context_from_object = True

        def get_object(self):
            return mock.Mock(project=project, module=None)

    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextGetObjectView, request)
    assert view.project == project


@pytest.mark.django_db
def test_project_mixin_project_object(rf, project):
    class FakeProjectContextGetObjectView(FakeProjectContextView):
        get_context_from_object = True

        def get_object(self):
            return project

    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextGetObjectView, request)
    assert view.project == project


@pytest.mark.django_db
def test_project_mixin_overwrite(rf, project):
    class FakeProjectContextGetProjectView(FakeProjectContextView):
        @property
        def project(self):
            return project

    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextGetProjectView,
                                   request)
    assert view.project == project


@pytest.mark.django_db
def test_project_mixin_module_kwargs(rf, module):
    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextView,
                                   request, module=module)
    assert view.module == module
    assert view.project == module.project


@pytest.mark.django_db
def test_project_mixin_module_url(rf, module):
    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextView,
                                   request,
                                   module_slug=module.slug)
    assert view.module == module


@pytest.mark.django_db
def test_project_mixin_module_url_overwrite(rf, module):
    class FakeProjectContextViewUrlOverwrite(FakeProjectContextView):
        module_lookup_field = 'id'
        module_url_kwarg = 'module_id'

    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextViewUrlOverwrite, request,
                                   module_id=module.id)
    assert view.module == module


@pytest.mark.django_db
def test_project_mixin_module_object(rf, module):
    class FakeProjectContextGetObjectView(FakeProjectContextView):
        get_context_from_object = True

        def get_object(self):
            return mock.Mock(module=module, project=None)

    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextGetObjectView, request)
    assert view.module == module


@pytest.mark.django_db
def test_project_mixin_module_object_module(rf, module):
    class FakeProjectContextGetObjectView(FakeProjectContextView):
        get_context_from_object = True

        def get_object(self):
            return module

    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextGetObjectView, request)
    assert view.module == module


@pytest.mark.django_db
def test_project_mixin_module_overwrite(rf, module):
    class FakeProjectContextGetProjectView(FakeProjectContextView):
        @property
        def module(self):
            return module

    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextGetProjectView, request)
    assert view.module == module


@pytest.mark.django_db
def test_project_mixin_template_context(rf, module):
    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextView,
                                   request, module=module)
    context = view.get_context_data()
    assert context['module'] == module
    assert context['project'] == module.project
