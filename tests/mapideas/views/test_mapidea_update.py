import pytest
from django.urls import reverse

from adhocracy4.test.helpers import redirect_target
from meinberlin.apps.mapideas import models
from meinberlin.apps.mapideas import phases
from meinberlin.test.helpers import freeze_phase
from meinberlin.test.helpers import setup_phase


@pytest.mark.django_db
def test_creator_can_update_during_active_phase(client,
                                                phase_factory,
                                                map_idea_factory,
                                                category_factory,
                                                area_settings_factory):
    phase, module, project, mapidea = setup_phase(
        phase_factory, map_idea_factory, phases.IssuePhase)
    area_settings_factory(module=module)
    category = category_factory(module=module)
    user = mapidea.creator
    url = reverse(
        'meinberlin_mapideas:mapidea-update',
        kwargs={
            'pk': mapidea.pk,
            'year': mapidea.created.year
        })
    with freeze_phase(phase):
        client.login(username=user.email, password='password')
        data = {
            'name': 'Another MapIdea',
            'description': 'changed description',
            'category': category.pk,
            'point': (0, 0),
            'point_label': 'somewhere'
        }
        response = client.post(url, data)
        assert redirect_target(response) == 'mapidea-detail'
        assert response.status_code == 302
        updated_mapidea = models.MapIdea.objects.get(id=mapidea.pk)
        assert updated_mapidea.description == 'changed description'


@pytest.mark.django_db
def test_creator_cannot_update_in_wrong_phase(client,
                                              phase_factory,
                                              map_idea_factory,
                                              category_factory):
    phase, module, project, mapidea = setup_phase(
        phase_factory, map_idea_factory, phases.RatingPhase)
    category = category_factory(module=module)
    user = mapidea.creator
    assert user not in project.moderators.all()
    url = reverse(
        'meinberlin_mapideas:mapidea-update',
        kwargs={
            'pk': mapidea.pk,
            'year': mapidea.created.year
        })
    with freeze_phase(phase):
        client.login(username=user.email, password='password')
        data = {
            'name': 'Another MapIdea',
            'description': 'changed description',
            'category': category.pk,
        }
        response = client.post(url, data)
        assert response.status_code == 403


@pytest.mark.django_db
def test_moderator_can_update_during_wrong_phase(client,
                                                 phase_factory,
                                                 map_idea_factory,
                                                 category_factory,
                                                 area_settings_factory):
    phase, module, project, mapidea = setup_phase(
        phase_factory, map_idea_factory, phases.RatingPhase)
    area_settings_factory(module=module)
    category = category_factory(module=module)
    user = mapidea.creator
    moderator = project.moderators.first()
    assert moderator is not user
    url = reverse(
        'meinberlin_mapideas:mapidea-update',
        kwargs={
            'pk': mapidea.pk,
            'year': mapidea.created.year
        })
    with freeze_phase(phase):
        client.login(username=moderator.email, password='password')
        data = {
            'name': 'Another MapIdea',
            'description': 'changed description',
            'category': category.pk,
            'point': (0, 0),
            'point_label': 'somewhere else'
        }
        response = client.post(url, data)
        assert redirect_target(response) == 'mapidea-detail'
        assert response.status_code == 302
        updated_mapidea = models.MapIdea.objects.get(id=mapidea.pk)
        assert updated_mapidea.description == 'changed description'


@pytest.mark.django_db
def test_creator_cannot_update(client, map_idea_factory):
    mapidea = map_idea_factory()
    user = mapidea.creator
    assert user not in mapidea.module.project.moderators.all()
    url = reverse(
        'meinberlin_mapideas:mapidea-update',
        kwargs={
            'pk': mapidea.pk,
            'year': mapidea.created.year
        })
    client.login(username=user.email, password='password')
    data = {
        'name': 'Another MapIdea',
        'description': 'changed description'
    }
    response = client.post(url, data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_moderators_can_always_update(client, phase_factory,
                                      map_idea_factory,
                                      category_factory,
                                      area_settings_factory):
    phase, module, project, mapidea = setup_phase(
        phase_factory, map_idea_factory, phases.RatingPhase)
    area_settings_factory(module=module)
    category = category_factory(module=module)
    user = mapidea.creator
    moderator = project.moderators.first()
    assert moderator is not user
    url = reverse(
        'meinberlin_mapideas:mapidea-update',
        kwargs={
            'pk': mapidea.pk,
            'year': mapidea.created.year
        })
    client.login(username=moderator.email, password='password')
    data = {
        'name': 'Another MapIdea',
        'description': 'changed description',
        'category': category.pk,
        'point': (0, 0),
        'point_label': 'somewhere'
    }
    response = client.post(url, data)
    assert redirect_target(response) == 'mapidea-detail'
    assert response.status_code == 302
    updated_mapidea = models.MapIdea.objects.get(id=mapidea.pk)
    assert updated_mapidea.description == 'changed description'
