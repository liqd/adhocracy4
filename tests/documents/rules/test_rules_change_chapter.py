import pytest
import rules

from adhocracy4.projects.enums import Access
from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import freeze_post_phase
from adhocracy4.test.helpers import freeze_pre_phase
from adhocracy4.test.helpers import setup_phase
from adhocracy4.test.helpers import setup_users
from meinberlin.apps.documents import phases
from tests.helpers import setup_group_users

perm_name = 'meinberlin_documents.change_chapter'


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_pre_phase(phase_factory, chapter_factory,
                   user_factory, group_factory,
                   user):

    phase, _, project, item = setup_phase(phase_factory, chapter_factory,
                                          phases.CommentPhase)

    creator = item.creator
    anonymous, moderator, initiator = setup_users(project)
    group_member_in_orga, group_member_out, group_member_in_project, project \
        = setup_group_users(user_factory, group_factory, project)

    assert project.is_public
    with freeze_pre_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, item)
        assert not rules.has_perm(perm_name, user, item)
        assert not rules.has_perm(perm_name, creator, item)
        assert not rules.has_perm(perm_name, group_member_in_orga, item)
        assert not rules.has_perm(perm_name, group_member_out, item)
        assert not rules.has_perm(perm_name, moderator, item)
        assert rules.has_perm(perm_name, group_member_in_project, item)
        assert rules.has_perm(perm_name, initiator, item)


@pytest.mark.django_db
def test_phase_active(phase_factory, chapter_factory,
                      user_factory, group_factory,
                      user):
    phase, _, project, item = setup_phase(phase_factory, chapter_factory,
                                          phases.CommentPhase)

    creator = item.creator
    anonymous, moderator, initiator = setup_users(project)
    group_member_in_orga, group_member_out, group_member_in_project, project \
        = setup_group_users(user_factory, group_factory, project)

    assert project.is_public
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, item)
        assert not rules.has_perm(perm_name, user, item)
        assert not rules.has_perm(perm_name, creator, item)
        assert not rules.has_perm(perm_name, group_member_in_orga, item)
        assert not rules.has_perm(perm_name, group_member_out, item)
        assert not rules.has_perm(perm_name, moderator, item)
        assert rules.has_perm(perm_name, group_member_in_project, item)
        assert rules.has_perm(perm_name, initiator, item)


@pytest.mark.django_db
def test_phase_active_project_private(phase_factory, chapter_factory,
                                      user_factory, group_factory,
                                      user):
    phase, _, project, item = setup_phase(
        phase_factory, chapter_factory, phases.CommentPhase,
        module__project__access=Access.PRIVATE)

    creator = item.creator
    anonymous, moderator, initiator = setup_users(project)
    participant = user_factory()
    project.participants.add(participant)
    group_member_in_orga, group_member_out, group_member_in_project, project \
        = setup_group_users(user_factory, group_factory, project)

    assert project.access == Access.PRIVATE
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, item)
        assert not rules.has_perm(perm_name, user, item)
        assert not rules.has_perm(perm_name, creator, item)
        assert not rules.has_perm(perm_name, participant, item)
        assert not rules.has_perm(perm_name, group_member_in_orga, item)
        assert not rules.has_perm(perm_name, group_member_out, item)
        assert not rules.has_perm(perm_name, moderator, item)
        assert rules.has_perm(perm_name, group_member_in_project, item)
        assert rules.has_perm(perm_name, initiator, item)


@pytest.mark.django_db
def test_phase_active_project_semipublic(phase_factory, chapter_factory,
                                         user_factory, group_factory,
                                         user):
    phase, _, project, item = setup_phase(
        phase_factory, chapter_factory, phases.CommentPhase,
        module__project__access=Access.SEMIPUBLIC)

    creator = item.creator
    anonymous, moderator, initiator = setup_users(project)
    participant = user_factory()
    project.participants.add(participant)
    group_member_in_orga, group_member_out, group_member_in_project, project \
        = setup_group_users(user_factory, group_factory, project)

    assert project.access == Access.SEMIPUBLIC
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, item)
        assert not rules.has_perm(perm_name, user, item)
        assert not rules.has_perm(perm_name, creator, item)
        assert not rules.has_perm(perm_name, participant, item)
        assert not rules.has_perm(perm_name, group_member_in_orga, item)
        assert not rules.has_perm(perm_name, group_member_out, item)
        assert not rules.has_perm(perm_name, moderator, item)
        assert rules.has_perm(perm_name, group_member_in_project, item)
        assert rules.has_perm(perm_name, initiator, item)


@pytest.mark.django_db
def test_phase_active_project_draft(phase_factory, chapter_factory,
                                    user_factory, group_factory,
                                    user):
    phase, _, project, item = setup_phase(phase_factory, chapter_factory,
                                          phases.CommentPhase,
                                          module__project__is_draft=True)

    creator = item.creator
    anonymous, moderator, initiator = setup_users(project)
    group_member_in_orga, group_member_out, group_member_in_project, project \
        = setup_group_users(user_factory, group_factory, project)

    assert project.is_draft
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, item)
        assert not rules.has_perm(perm_name, user, item)
        assert not rules.has_perm(perm_name, creator, item)
        assert not rules.has_perm(perm_name, group_member_in_orga, item)
        assert not rules.has_perm(perm_name, group_member_out, item)
        assert not rules.has_perm(perm_name, moderator, item)
        assert rules.has_perm(perm_name, group_member_in_project, item)
        assert rules.has_perm(perm_name, initiator, item)


@pytest.mark.django_db
def test_post_phase_project_archived(phase_factory, chapter_factory,
                                     user_factory, group_factory,
                                     user):
    phase, _, project, item = setup_phase(phase_factory, chapter_factory,
                                          phases.CommentPhase,
                                          module__project__is_archived=True)

    creator = item.creator
    anonymous, moderator, initiator = setup_users(project)
    group_member_in_orga, group_member_out, group_member_in_project, project \
        = setup_group_users(user_factory, group_factory, project)

    assert project.is_archived
    with freeze_post_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, item)
        assert not rules.has_perm(perm_name, user, item)
        assert not rules.has_perm(perm_name, creator, item)
        assert not rules.has_perm(perm_name, group_member_in_orga, item)
        assert not rules.has_perm(perm_name, group_member_out, item)
        assert not rules.has_perm(perm_name, moderator, item)
        assert rules.has_perm(perm_name, group_member_in_project, item)
        assert rules.has_perm(perm_name, initiator, item)
