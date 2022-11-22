import pytest
import rules
from django.contrib.auth.models import AnonymousUser

from meinberlin.test.helpers import setup_group_members

perm_name = 'meinberlin_bplan.add_bplan'

# This permission is used in the API, not in the views.


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_add(project, user_factory, group_factory, admin):
    anonymous = AnonymousUser()
    user = user_factory()
    project, group_member_in_org, group_member_in_pro, group_member_out = \
        setup_group_members(project, group_factory, user_factory)
    organisation = project.organisation
    initiator = organisation.initiators.first()

    assert not rules.has_perm(perm_name, anonymous, organisation)
    assert not rules.has_perm(perm_name, user, organisation)
    assert rules.has_perm(perm_name, initiator, organisation)
    assert not rules.has_perm(perm_name, group_member_in_pro, organisation)
    assert not rules.has_perm(perm_name, group_member_in_org, organisation)
    assert not rules.has_perm(perm_name, group_member_out, organisation)
    assert not rules.has_perm(perm_name, admin, organisation)
