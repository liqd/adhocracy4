import pytest
import rules
from django.contrib.auth.models import AnonymousUser

from meinberlin.test.helpers import setup_group_member

perm_name = 'meinberlin_bplan.add_bplan'

# This permission is used in the API, not in the views.


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_add(organisation, user_factory, group_factory, admin):
    anonymous = AnonymousUser()
    user = user_factory()
    initiator = organisation.initiators.first()
    group_member, organisation, _ = setup_group_member(
        organisation, None, group_factory, user_factory)

    assert not rules.has_perm(perm_name, anonymous, organisation)
    assert not rules.has_perm(perm_name, user, organisation)
    assert rules.has_perm(perm_name, initiator, organisation)
    assert not rules.has_perm(perm_name, group_member, organisation)
    assert not rules.has_perm(perm_name, admin, organisation)
