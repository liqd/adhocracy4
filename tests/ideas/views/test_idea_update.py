import pytest
from django.urls import reverse

from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import redirect_target
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.ideas import models
from meinberlin.apps.ideas import phases


@pytest.mark.django_db
def test_creator_can_update_during_active_phase(client,
                                                phase_factory,
                                                idea_factory,
                                                category_factory):
    phase, module, project, idea = setup_phase(
        phase_factory, idea_factory, phases.IssuePhase)
    category = category_factory(module=module)
    user = idea.creator
    url = reverse(
        'meinberlin_ideas:idea-update',
        kwargs={
            'pk': idea.pk,
            'year': idea.created.year
        })
    with freeze_phase(phase):
        client.login(username=user.email, password='password')
        data = {
            'name': 'Another Idea',
            'description': 'changed description',
            'category': category.pk,
        }
        response = client.post(url, data)
        assert redirect_target(response) == 'idea-detail'
        assert response.status_code == 302
        updated_idea = models.Idea.objects.get(id=idea.pk)
        assert updated_idea.description == 'changed description'


@pytest.mark.django_db
def test_creator_cannot_update_in_wrong_phase(client,
                                              phase_factory,
                                              idea_factory,
                                              category_factory):
    phase, module, project, idea = setup_phase(
        phase_factory, idea_factory, phases.RatingPhase)
    category = category_factory(module=module)
    user = idea.creator
    assert user not in project.moderators.all()
    url = reverse(
        'meinberlin_ideas:idea-update',
        kwargs={
            'pk': idea.pk,
            'year': idea.created.year
        })
    with freeze_phase(phase):
        client.login(username=user.email, password='password')
        data = {
            'name': 'Another Idea',
            'description': 'changed description',
            'category': category.pk,
        }
        response = client.post(url, data)
        assert response.status_code == 403


@pytest.mark.django_db
def test_moderator_can_update_during_wrong_phase(client,
                                                 phase_factory,
                                                 idea_factory,
                                                 category_factory):
    phase, module, project, idea = setup_phase(
        phase_factory, idea_factory, phases.RatingPhase)
    category = category_factory(module=module)
    user = idea.creator
    moderator = project.moderators.first()
    assert moderator is not user
    url = reverse(
        'meinberlin_ideas:idea-update',
        kwargs={
            'pk': idea.pk,
            'year': idea.created.year
        })
    with freeze_phase(phase):
        client.login(username=moderator.email, password='password')
        data = {
            'name': 'Another Idea',
            'description': 'changed description',
            'category': category.pk,
        }
        response = client.post(url, data)
        assert redirect_target(response) == 'idea-detail'
        assert response.status_code == 302
        updated_idea = models.Idea.objects.get(id=idea.pk)
        assert updated_idea.description == 'changed description'


@pytest.mark.django_db
def test_creator_cannot_update(client, idea_factory):
    idea = idea_factory()
    user = idea.creator
    assert user not in idea.module.project.moderators.all()
    url = reverse(
        'meinberlin_ideas:idea-update',
        kwargs={
            'pk': idea.pk,
            'year': idea.created.year
        })
    client.login(username=user.email, password='password')
    data = {
        'name': 'Another Idea',
        'description': 'changed description'
    }
    response = client.post(url, data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_moderators_can_always_update(client, idea_factory):
    idea = idea_factory()
    moderator = idea.module.project.moderators.first()
    assert moderator is not idea.creator
    url = reverse(
        'meinberlin_ideas:idea-update',
        kwargs={
            'pk': idea.pk,
            'year': idea.created.year
        })
    client.login(username=moderator.email, password='password')
    data = {
        'name': 'Another Idea',
        'description': 'changed description'
    }
    response = client.post(url, data)
    assert redirect_target(response) == 'idea-detail'
    assert response.status_code == 302
    updated_idea = models.Idea.objects.get(id=idea.pk)
    assert updated_idea.description == 'changed description'
