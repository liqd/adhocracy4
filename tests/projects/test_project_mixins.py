import pytest
from datetime import timedelta
from django.http import HttpResponse
from django.views.generic import ListView, View
from freezegun import freeze_time
from tests.apps.questions import models as question_models

from adhocracy4.projects import mixins, models
from adhocracy4.test.helpers import redirect_target


@pytest.fixture
def user_request(rf, user):
    request = rf.get('/url')
    request.user = user
    return request


@pytest.fixture
def project_detail_view():
    class FakeProjectDetailView(mixins.ModuleDispatchMixin, View):
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
def test_module_dispatch_mixin_module_active(
        user_request, project_detail_view, phase):
    module = phase.module
    project = module.project

    with freeze_time(phase.start_date):
        response = project_detail_view(user_request, slug=project.slug)
        assert redirect_target(response) == 'module-detail'
        assert response.url == module.get_absolute_url()


@pytest.mark.django_db
def test_module_dispatch_mixin_after_finish(user_request, project_detail_view,
                                            phase):
    module = phase.module
    project = module.project
    with freeze_time(phase.end_date + timedelta(days=1)):
        response = project_detail_view(user_request, slug=project.slug)
        assert redirect_target(response) == 'module-detail'
        assert response.url == module.get_absolute_url()


@pytest.mark.django_db
def test_phase_dispatch_mixin_default(user_request, project_detail_view,
                                      project):
    response = project_detail_view(user_request, slug=project.slug)
    assert response.content == b'project_detail'


@pytest.mark.django_db
def test_project_mixin(rf, question_list_view, phase):
    project = phase.module.project
    request = rf.get('/project_name/ideas')
    response = question_list_view(request, project=project)
    view_data = response.context_data['view']
    assert view_data.project == project
    assert view_data.phase == phase
