import pytest
from django.urls import reverse

from meinberlin.apps.livequestions import phases
from meinberlin.apps.livequestions.models import LiveQuestion
from meinberlin.test.helpers import assert_template_response
from meinberlin.test.helpers import freeze_phase
from meinberlin.test.helpers import freeze_post_phase
from meinberlin.test.helpers import freeze_pre_phase


@pytest.mark.django_db
def test_anonymous_can_create_livequestion_during_active_phase(
        client, category_factory, phase_factory):

    phase = phase_factory(phase_content=phases.IssuePhase())
    module = phase.module
    category = category_factory(module=module)
    url = reverse('meinberlin_livequestions:question-create',
                  kwargs={'slug': module.slug})
    data = {
        'text': 'I have a question',
        'category': category.pk
    }
    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(
            response, 'meinberlin_livequestions/livequestion_form.html')
        assert response.context_data['slug'] == module.slug
        assert response.context_data['project'] == module.project
        assert response.context_data['mode'] == 'create'

        response = client.post(url, data)
        assert response.status_code == 302

    live_question = LiveQuestion.objects.first()
    assert live_question.text == 'I have a question'
    assert live_question.category == category


@pytest.mark.django_db
def test_user_cannot_create_livequestion_during_pre_phase(
        client, user, category_factory, phase_factory):

    phase = phase_factory(phase_content=phases.IssuePhase())
    module = phase.module
    category = category_factory(module=module)
    url = reverse('meinberlin_livequestions:question-create',
                  kwargs={'slug': module.slug})
    data = {
        'text': 'I have a question',
        'category': category.pk
    }
    assert client.login(username=user.email, password='password')
    with freeze_pre_phase(phase):
        response = client.post(url, data)
        assert response.status_code == 403


@pytest.mark.django_db
def test_initiator_cannot_create_livequestion_during_post_phase(
        client, category_factory, phase_factory):

    phase = phase_factory(phase_content=phases.IssuePhase())
    module = phase.module
    category = category_factory(module=module)
    initiator = module.project.organisation.initiators.first()
    url = reverse('meinberlin_livequestions:question-create',
                  kwargs={'slug': module.slug})
    data = {
        'text': 'I have a question',
        'category': category.pk
    }
    assert client.login(username=initiator.email, password='password')
    with freeze_post_phase(phase):
        response = client.post(url, data)
        assert response.status_code == 403
