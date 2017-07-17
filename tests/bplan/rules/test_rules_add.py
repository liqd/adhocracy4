import pytest
import rules
from django.contrib.auth.models import AnonymousUser

perm_name = 'meinberlin_bplan.add_bplan'


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_add(organisation, user):
    anonymous = AnonymousUser()
    initiator = organisation.initiators.first()

    assert not rules.has_perm(perm_name, anonymous, organisation)
    assert not rules.has_perm(perm_name, user, organisation)
    assert rules.has_perm(perm_name, initiator, organisation)
