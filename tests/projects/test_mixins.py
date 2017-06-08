import pytest
from dateutil.parser import parse
from django.http import HttpResponse
from django.views.generic import ListView, View
from freezegun import freeze_time
from tests.apps.questions import models as question_models

from adhocracy4.projects import mixins, models


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
    phase = project.phases.first()

    with freeze_time(phase.end_date):
        request = rf.get('/url')
        response = project_detail_view(request, slug=project.slug)
        assert response.content == b'project_detail'


@pytest.mark.django_db
def test_project_mixin(rf, question_list_view, phase):
    project = phase.module.project
    request = rf.get('/project_name/ideas')

    with freeze_time(phase.start_date):
        response = question_list_view(request, project=project)

    response = question_list_view(request, project=project)
    view_data = response.context_data['view']
    assert view_data.project == project
    assert view_data.phase == phase


@pytest.mark.django_db
def test_project_inject_phase_after_finish(rf, project,
                                           question_list_view):
    module = project.module_set.first()
    phase = module.phase_set.first()

    request = rf.get('/project_name/ideas')

    with freeze_time(phase.end_date):
        response = question_list_view(request, project=project)

    response = question_list_view(request, project=project)
    view_data = response.context_data['view']
    assert view_data.project == project
    assert view_data.phase == phase
