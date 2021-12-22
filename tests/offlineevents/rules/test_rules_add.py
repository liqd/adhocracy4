import pytest
import rules

from adhocracy4.test.helpers import setup_users

perm_name = 'meinberlin_offlineevents.add_offlineevent'


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_rule(offline_event, user):
    project = offline_event.project
    anonymous, moderator, initiator = setup_users(project)

    assert not rules.has_perm(perm_name, anonymous, project)
    assert not rules.has_perm(perm_name, user, project)
    assert not rules.has_perm(perm_name, moderator, project)
    assert rules.has_perm(perm_name, initiator, project)
