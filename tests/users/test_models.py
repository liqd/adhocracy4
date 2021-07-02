import pytest
from django.contrib import auth

from adhocracy4.test.helpers import setup_users

User = auth.get_user_model()


@pytest.mark.django_db
def test_absolute_url(user):
    with pytest.raises(AttributeError):
        user.get_absolute_url()


@pytest.mark.django_db
def test_short_name(user):
    assert user.get_short_name() == user.username


@pytest.mark.django_db
def test_full_name(user):
    assert user.get_full_name() == \
        ('%s <%s>' % (user.username, user.email)).strip()


@pytest.mark.django_db
def test_organisations(user_factory, project_factory, group_factory,
                       organisation_factory):
    group1 = group_factory()
    group2 = group_factory()
    organisation1 = organisation_factory()
    organisation1.groups.add(group1)
    organisation2 = organisation_factory()
    organisation2.groups.add(group2)
    project = project_factory(organisation=organisation1)
    anonymous, moderator, initiator = setup_users(project)
    user = user_factory()
    group_member1 = user_factory.create(groups=(group1, ))
    group_member2 = user_factory.create(groups=(group2, ))

    assert organisation1 not in user.organisations
    assert organisation2 not in user.organisations
    assert organisation1 not in moderator.organisations
    assert organisation2 not in moderator.organisations
    assert organisation1 in initiator.organisations
    assert organisation2 not in initiator.organisations
    assert organisation1 in group_member1.organisations
    assert organisation2 not in group_member1.organisations
    assert organisation1 not in group_member2.organisations
    assert organisation2 in group_member2.organisations
