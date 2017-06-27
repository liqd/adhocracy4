import pytest
from django.http import HttpResponse
from django.views.generic import View
from freezegun import freeze_time

from adhocracy4.projects import models, views


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
