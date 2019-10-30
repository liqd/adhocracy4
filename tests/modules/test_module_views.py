from datetime import timedelta

import pytest
from dateutil.parser import parse
from freezegun import freeze_time

from adhocracy4.modules.views import ModuleDetailView
from adhocracy4.test.helpers import redirect_target
from tests.apps.questions.views import QuestionList


@pytest.mark.django_db
def test_detail_view_module(rf, user, phase_factory, module_factory):
    module = module_factory()
    phase = phase_factory(
        module=module,
        start_date=parse('2013-01-01 00:00:00 UTC'),
        end_date=parse('2013-01-02 00:00:00 UTC')
    )
    module2 = module_factory(project=module.project)
    phase2 = phase_factory(
        module=module2,
        start_date=parse('2013-01-03 00:00:00 UTC'),
        end_date=parse('2013-01-04 00:00:00 UTC')
    )
    request = rf.get('/url')
    request.user = user
    with freeze_time(phase.start_date - timedelta(days=1)):
        response = ModuleDetailView.as_view()(request, module_slug=module.slug)
        assert response.status_code == 200
        assert isinstance(response.context_data.get('view'), ModuleDetailView)
        response = ModuleDetailView.as_view()(request,
                                              module_slug=module2.slug)
        assert response.status_code == 200
        assert isinstance(response.context_data.get('view'), ModuleDetailView)
    with freeze_time(phase.end_date):
        response = ModuleDetailView.as_view()(request, module_slug=module.slug)
        assert redirect_target(response) == 'project-detail'
        response = ModuleDetailView.as_view()(request,
                                              module_slug=module2.slug)
        assert response.status_code == 200
        assert isinstance(response.context_data.get('view'), ModuleDetailView)
    with freeze_time(phase2.start_date):
        response = ModuleDetailView.as_view()(request, module_slug=module.slug)
        assert response.status_code == 200
        assert isinstance(response.context_data.get('view'), QuestionList)
        response = ModuleDetailView.as_view()(request,
                                              module_slug=module2.slug)
        assert redirect_target(response) == 'project-detail'
    with freeze_time(phase2.end_date):
        response = ModuleDetailView.as_view()(request, module_slug=module.slug)
        assert response.status_code == 200
        assert isinstance(response.context_data.get('view'), QuestionList)
        response = ModuleDetailView.as_view()(request,
                                              module_slug=module2.slug)
        assert redirect_target(response) == 'project-detail'
