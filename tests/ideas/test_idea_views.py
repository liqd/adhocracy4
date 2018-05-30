import pytest
from django.core.urlresolvers import reverse

from adhocracy4.test.helpers import redirect_target
from meinberlin.apps.ideas import models
from meinberlin.apps.ideas import phases
from meinberlin.apps.ideas import views
from meinberlin.test.helpers import assert_template_response
from meinberlin.test.helpers import freeze_phase
from meinberlin.test.helpers import setup_phase


@pytest.mark.django_db
def test_list_view(rf, phase_factory, idea_factory):
    phase, module, project, idea = setup_phase(
        phase_factory, idea_factory, phases.FeedbackPhase)
    phase_2, module_2, project_2, idea_2 = setup_phase(
        phase_factory, idea_factory, phases.FeedbackPhase)

    with freeze_phase(phase):
        view = views.IdeaListView.as_view()
        request = rf.get('/ideas')
        response = view(request, project=project, module=module)

        assert idea in response.context_data['idea_list']
        assert idea_2 not in response.context_data['idea_list']
        assert response.context_data['idea_list'][0].comment_count == 0
        assert response.context_data['idea_list'][0].positive_rating_count == 0
        assert response.context_data['idea_list'][0].negative_rating_count == 0


@pytest.mark.django_db
@pytest.mark.parametrized('idea__module__project__is_public', [False])
def test_detail_view_private(client, user, phase_factory, idea_factory):
    phase, module, project, idea = setup_phase(
        phase_factory, idea_factory, phases.FeedbackPhase)
    idea.module.project.is_public = False
    idea.module.project.save()
    url = idea.get_absolute_url()
    response = client.get(url)
    assert response.status_code == 302
    assert redirect_target(response) == 'account_login'

    idea.module.project.participants.add(user)
    client.login(username=user.email,
                 password='password')
    response = client.get(url)
    assert response.status_code == 200

    user = idea.project.moderators.first()
    client.login(username=user.email,
                 password='password')
    response = client.get(url)
    assert response.status_code == 200

    user = idea.project.organisation.initiators.first()
    client.login(username=user.email,
                 password='password')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_view(client, phase_factory, user,
                     category_factory):
    phase = phase_factory(phase_content=phases.IssuePhase())
    module = phase.module
    category = category_factory(module=module)
    url = reverse('meinberlin_ideas:idea-create',
                  kwargs={'module_slug': module.slug})
    with freeze_phase(phase):
        count = models.Idea.objects.all().count()
        assert count == 0
        response = client.get(url)
        assert response.status_code == 302
        assert redirect_target(response) == 'account_login'
        client.login(username=user.email, password='password')
        response = client.get(url)
        assert response.status_code == 200
        idea = {
            'name': 'Idea',
            'description': 'description',
            'category': category.pk,
        }
        response = client.post(url, idea)
        assert response.status_code == 302
        assert redirect_target(response) == 'idea-detail'
        count = models.Idea.objects.all().count()
        assert count == 1


@pytest.mark.django_db
def test_create_view_wrong_phase(client, phase_factory, idea_factory, user):
    phase = phase_factory(phase_content=phases.RatingPhase())
    module = phase.module
    url = reverse('meinberlin_ideas:idea-create',
                  kwargs={'module_slug': module.slug})
    with freeze_phase(phase):
        response = client.get(url)
        assert response.status_code == 302
        client.login(username=user.email, password='password')
        response = client.get(url)
        assert response.status_code == 403


@pytest.mark.django_db
def test_update_view(client, phase_factory, idea_factory, user,
                     category_factory):
    phase, module, project, idea = setup_phase(
        phase_factory, idea_factory, phases.IssuePhase)
    category = category_factory(module=module)
    url = reverse(
        'meinberlin_ideas:idea-update',
        kwargs={
            'pk': idea.pk,
            'year': idea.created.year
        })
    with freeze_phase(phase):
        client.login(username=idea.creator.email, password='password')

        response = client.get(url)
        assert_template_response(
            response, 'meinberlin_ideas/idea_update_form.html')

        idea = {
            'name': 'Another Idea',
            'description': 'changed description',
            'category': category.pk,
        }
        response = client.post(url, idea)
        assert redirect_target(response) == 'idea-detail'


@pytest.mark.django_db
def test_delete_view(client, phase_factory, idea_factory, user,
                     category_factory):
    phase, module, project, idea = setup_phase(
        phase_factory, idea_factory, phases.IssuePhase)
    url = reverse(
        'meinberlin_ideas:idea-delete',
        kwargs={
            'pk': idea.pk,
            'year': idea.created.year
        })
    with freeze_phase(phase):
        client.login(username=idea.creator.email, password='password')

        response = client.get(url)
        assert_template_response(
            response, 'meinberlin_ideas/idea_confirm_delete.html')

        response = client.post(url)
        assert redirect_target(response) == 'project-detail'
