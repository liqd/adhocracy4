import pytest
from dateutil.parser import parse
from django.views.generic import ListView
from freezegun import freeze_time
from tests.apps.questions import models as question_models

from adhocracy4.projects import mixins


@pytest.fixture
def question_list_view():
    class DummyView(mixins.ProjectMixin, ListView):
        model = question_models.Question
    return DummyView.as_view()


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
        response = question_list_view(request, project=project)

    response = question_list_view(request, project=project)
    view_data = response.context_data['view']
    assert view_data.project == project
    assert view_data.phase == phase
