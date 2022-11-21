import pytest
import rules

from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import freeze_post_phase
from adhocracy4.test.helpers import freeze_pre_phase
from adhocracy4.test.helpers import setup_phase
from adhocracy4.test.helpers import setup_users
from meinberlin.apps.bplan import phases
from meinberlin.test.helpers import setup_group_members

perm_name = 'meinberlin_bplan.add_statement'


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_pre_phase(phase_factory, user, admin, user_factory, group_factory):
    phase, module, project, _ = setup_phase(phase_factory, None,
                                            phases.StatementPhase)
    anonymous, moderator, initiator = setup_users(project)
    project, group_member_in_org, group_member_in_pro, group_member_out = \
        setup_group_members(project, group_factory, user_factory)

    assert project.is_public
    with freeze_pre_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert not rules.has_perm(perm_name, group_member_out, module)
        assert not rules.has_perm(perm_name, group_member_in_org, module)
        assert not rules.has_perm(perm_name, group_member_in_pro, module)
        assert not rules.has_perm(perm_name, moderator, module)
        assert not rules.has_perm(perm_name, initiator, module)
        assert not rules.has_perm(perm_name, admin, module)


@pytest.mark.django_db
def test_active(phase_factory, user, admin, user_factory, group_factory):
    phase, module, project, _ = setup_phase(phase_factory, None,
                                            phases.StatementPhase)
    anonymous, moderator, initiator = setup_users(project)
    project, group_member_in_org, group_member_in_pro, group_member_out = \
        setup_group_members(project, group_factory, user_factory)

    assert project.is_public
    with freeze_phase(phase):
        assert rules.has_perm(perm_name, anonymous, module)
        assert rules.has_perm(perm_name, user, module)
        assert rules.has_perm(perm_name, group_member_out, module)
        assert rules.has_perm(perm_name, group_member_in_org, module)
        assert rules.has_perm(perm_name, group_member_in_pro, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)
        assert rules.has_perm(perm_name, admin, module)


@pytest.mark.django_db
def test_post_phase(phase_factory, user, admin, user_factory, group_factory):
    phase, module, project, _ = setup_phase(phase_factory, None,
                                            phases.StatementPhase)
    anonymous, moderator, initiator = setup_users(project)
    project, group_member_in_org, group_member_in_pro, group_member_out = \
        setup_group_members(project, group_factory, user_factory)

    assert project.is_public
    with freeze_post_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert not rules.has_perm(perm_name, group_member_out, module)
        assert not rules.has_perm(perm_name, group_member_in_org, module)
        assert not rules.has_perm(perm_name, group_member_in_pro, module)
        assert not rules.has_perm(perm_name, moderator, module)
        assert not rules.has_perm(perm_name, initiator, module)
        assert not rules.has_perm(perm_name, admin, module)
