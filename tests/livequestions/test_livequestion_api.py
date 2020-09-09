import pytest
from django.urls import reverse

from meinberlin.apps.livequestions import models
from meinberlin.apps.livequestions import phases
from meinberlin.test.helpers import setup_phase


@pytest.mark.django_db
def test_anonymous_can_view_and_cannot_change_questions(apiclient,
                                                        phase_factory,
                                                        live_question_factory):
    phase, module, project, live_question = setup_phase(phase_factory,
                                                        live_question_factory,
                                                        phases.IssuePhase)

    url = reverse('questions-list', kwargs={'module_pk': module.pk})
    url_detail = reverse('questions-detail',
                         kwargs={'module_pk': module.pk,
                                 'pk': live_question.pk})

    data = {
        'text': live_question.text,
        'category': live_question.category.pk,
        'is_hidden': True
    }

    response = apiclient.get(url)
    assert response.status_code == 200

    response = apiclient.put(url_detail, data, format='json')
    assert response.status_code == 403


@pytest.mark.django_db
def test_moderator_can_view_and_change_questions(apiclient,
                                                 phase_factory,
                                                 live_question_factory):
    phase, module, project, live_question = setup_phase(phase_factory,
                                                        live_question_factory,
                                                        phases.IssuePhase)

    url = reverse('questions-list', kwargs={'module_pk': module.pk})
    url_detail = reverse('questions-detail',
                         kwargs={'module_pk': module.pk,
                                 'pk': live_question.pk})

    data = {
        'text': live_question.text,
        'category': live_question.category.pk,
        'is_hidden': True
    }

    moderator = project.moderators.first()
    apiclient.force_authenticate(user=moderator)

    response = apiclient.get(url)
    assert response.status_code == 200

    assert len(models.LiveQuestion.objects.filter(is_hidden=True)) == 0
    response = apiclient.put(url_detail, data, format='json')
    assert response.status_code == 200

    assert len(models.LiveQuestion.objects.all()) == 1
    live_question_changed = models.LiveQuestion.objects.first()
    assert live_question_changed.is_hidden
