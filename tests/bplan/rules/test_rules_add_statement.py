import pytest
import rules

from apps.bplan import phases
from tests.helpers import freeze_pre_phase
from tests.helpers import setup_phase
from tests.helpers import setup_users

perm_name = 'meinberlin_bplan.add_statement'


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_rule(phase_factory, user):
    phase, module, project, _ = setup_phase(phase_factory, None,
                                            phases.StatementPhase)
    anonymous, moderator, initiator = setup_users(project)

    assert project.is_public
    with freeze_pre_phase(phase):
        assert rules.has_perm(perm_name, anonymous, module)
        assert rules.has_perm(perm_name, user, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)
