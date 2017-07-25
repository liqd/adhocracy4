import pytest
from django.http import HttpResponse
from django.views.generic import View
from freezegun import freeze_time

from adhocracy4.modules import mixins
from adhocracy4.modules import models


@pytest.fixture
def module_detail_view():
    class FakeModuleDetailView(mixins.PhaseDispatchMixin, View):
        model = models.Module

        def get(self, request, *args, **kwargs):
            return HttpResponse('module_detail')
    return FakeModuleDetailView.as_view()


@pytest.mark.django_db
def test_phase_dispatch_mixin_phase(rf, module_detail_view, phase):
    module = phase.module
    with freeze_time(phase.start_date):
        request = rf.get('/url')
        response = module_detail_view(request, slug=module.slug)
        assert 'a4test_questions/question_list.html' in response.template_name


@pytest.mark.django_db
def test_phase_dispatch_mixin_phase_after_finish(
        rf, module_detail_view, phase):
    module = phase.module
    with freeze_time(phase.end_date):
        request = rf.get('/url')
        response = module_detail_view(request, slug=module.slug)
        assert 'a4test_questions/question_list.html' in response.template_name


@pytest.mark.django_db
def test_phase_dispatch_mixin_default(rf, module_detail_view, module):
    request = rf.get('/url')
    response = module_detail_view(request, slug=module.slug)
    assert response.content == b'module_detail'
