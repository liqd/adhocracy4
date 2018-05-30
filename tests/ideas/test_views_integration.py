import pytest
from django.core.urlresolvers import reverse

from adhocracy4.test.helpers import redirect_target
from meinberlin.apps.ideas import phases
from meinberlin.test.helpers import assert_template_response
from meinberlin.test.helpers import freeze_phase
from meinberlin.test.helpers import setup_phase


@pytest.mark.django_db
def test_list_view(client, phase_factory, idea_factory):
    phase, module, project, idea = setup_phase(
        phase_factory, idea_factory, phases.FeedbackPhase)
    url = project.get_absolute_url()
    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(
            response, 'meinberlin_ideas/idea_list.html')


@pytest.mark.django_db
def test_detail_view(client, phase_factory, idea_factory):
    phase, module, project, idea = setup_phase(
        phase_factory, idea_factory, phases.FeedbackPhase)
    url = idea.get_absolute_url()
    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(
            response, 'meinberlin_ideas/idea_detail.html')


@pytest.mark.django_db
def test_create_view(client, phase_factory, idea_factory, user,
                     category_factory):
    phase, module, project, idea = setup_phase(
        phase_factory, idea_factory, phases.IssuePhase)
    category = category_factory(module=module)
    url = reverse('meinberlin_ideas:idea-create',
                  kwargs={'module_slug': module.slug})
    with freeze_phase(phase):
        client.login(username=user.email, password='password')

        response = client.get(url)
        assert_template_response(
            response, 'meinberlin_ideas/idea_create_form.html')

        idea = {
            'name': 'Idea',
            'description': 'description',
            'category': category.pk,
        }
        response = client.post(url, idea)
        assert redirect_target(response) == 'idea-detail'
