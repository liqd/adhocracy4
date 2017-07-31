import pytest
from datetime import timedelta
from freezegun import freeze_time

from adhocracy4.modules.views import ModuleDetailView
from adhocracy4.test.helpers import redirect_target

from tests.apps.questions.views import QuestionList


@pytest.mark.django_db
def test_detail_view_module(rf, user, phase):
    module = phase.module
    request = rf.get('/url')
    request.user = user
    with freeze_time(phase.start_date - timedelta(days=1)):
        response = ModuleDetailView.as_view()(request, module_slug=module.slug)
        view = response.context_data.get('view')
        assert response.status_code == 200
        assert isinstance(view, ModuleDetailView)
    with freeze_time(phase.start_date):
        response = ModuleDetailView.as_view()(request, module_slug=module.slug)
        assert redirect_target(response) == 'project-detail'
    with freeze_time(phase.end_date):
        response = ModuleDetailView.as_view()(request, module_slug=module.slug)
        view = response.context_data.get('view')
        assert response.status_code == 200
        assert isinstance(view, QuestionList)
