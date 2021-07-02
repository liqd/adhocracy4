import pytest
from django.urls import reverse

from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.likes.models import Like
from meinberlin.apps.livequestions import phases
from meinberlin.test.helpers import assert_template_response


@pytest.mark.django_db
def test_presentation_list_view(client, user, phase_factory,
                                like_factory, live_question_factory):
    phase, module, project, live_question = setup_phase(
        phase_factory, live_question_factory, phases.IssuePhase)
    phase_2, module_2, project_2, live_question_2 = setup_phase(
        phase_factory, live_question_factory, phases.IssuePhase)

    like_factory(question=live_question)
    assert Like.objects.all().count() == \
           len(live_question.question_likes.all())

    url = reverse('meinberlin_livequestions:question-present',
                  kwargs={'module_slug': module.slug})

    moderator = module.project.moderators.first()

    with freeze_phase(phase):
        response = client.get(url)
        assert response.status_code == 302
        assert response.url == '/accounts/login/?next=' + url

        client.login(username=user.email, password='password')
        response = client.get(url)
        assert response.status_code == 403

        client.login(username=moderator.email, password='password')
        response = client.get(url)
        assert_template_response(
            response, 'meinberlin_livequestions/question_present_list.html')

        assert live_question in response.context_data['livequestion_list']
        assert live_question_2 not in \
               response.context_data['livequestion_list']

        assert len(response.context_data['object_list'].all()) == 1
        assert response.context_data['object_list'][0] == live_question
