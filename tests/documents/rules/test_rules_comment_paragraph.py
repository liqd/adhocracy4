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

perm_name = 'meinberlin_documents.comment_paragraph'


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_pre_phase(phase_factory, chapter_factory, paragraph_factory,
                   user_factory, group_factory, user):
    phase, _, project, item = setup_phase(phase_factory, chapter_factory,
                                          phases.CommentPhase)

    anonymous, moderator, initiator = setup_users(project)
    group_member_in_orga, group_member_out, group_member_in_project, project \
        = setup_group_users(user_factory, group_factory, project)

    paragraph = paragraph_factory(chapter=item)

    assert project.access == Access.PUBLIC
    with freeze_pre_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, paragraph)
        assert not rules.has_perm(perm_name, user, paragraph)
        assert not rules.has_perm(perm_name, group_member_in_orga, paragraph)
        assert not rules.has_perm(perm_name, group_member_out, paragraph)
        assert rules.has_perm(perm_name, group_member_in_project, paragraph)
        assert rules.has_perm(perm_name, moderator, paragraph)
        assert rules.has_perm(perm_name, initiator, paragraph)


@pytest.mark.django_db
def test_phase_active(phase_factory, chapter_factory, paragraph_factory,
                      user_factory, group_factory, user):
    phase, _, project, item = setup_phase(phase_factory, chapter_factory,
                                          phases.CommentPhase)

    anonymous, moderator, initiator = setup_users(project)
    group_member_in_orga, group_member_out, group_member_in_project, project \
        = setup_group_users(user_factory, group_factory, project)

    paragraph = paragraph_factory(chapter=item)

    assert project.access == Access.PUBLIC
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, paragraph)
        assert rules.has_perm(perm_name, user, paragraph)
        assert rules.has_perm(perm_name, group_member_in_orga, paragraph)
        assert rules.has_perm(perm_name, group_member_out, paragraph)
        assert rules.has_perm(perm_name, group_member_in_project, paragraph)
        assert rules.has_perm(perm_name, moderator, paragraph)
        assert rules.has_perm(perm_name, initiator, paragraph)


@pytest.mark.django_db
def test_phase_active_project_private(phase_factory, chapter_factory,
                                      paragraph_factory, user_factory,
                                      group_factory, user):
    phase, _, project, item = setup_phase(
        phase_factory, chapter_factory, phases.CommentPhase,
        module__project__access=Access.PRIVATE)

    anonymous, moderator, initiator = setup_users(project)
    participant = user_factory()
    project.participants.add(participant)
    group_member_in_orga, group_member_out, group_member_in_project, project \
        = setup_group_users(user_factory, group_factory, project)

    paragraph = paragraph_factory(chapter=item)

    assert project.access == Access.PRIVATE
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, paragraph)
        assert not rules.has_perm(perm_name, user, paragraph)
        assert not rules.has_perm(perm_name, group_member_in_orga, paragraph)
        assert not rules.has_perm(perm_name, group_member_out, paragraph)
        assert rules.has_perm(perm_name, group_member_in_project, paragraph)
        assert rules.has_perm(perm_name, participant, paragraph)
        assert rules.has_perm(perm_name, moderator, paragraph)
        assert rules.has_perm(perm_name, initiator, paragraph)


@pytest.mark.django_db
def test_phase_active_project_semipublic(phase_factory, chapter_factory,
                                         paragraph_factory, user_factory,
                                         group_factory, user):
    phase, _, project, item = setup_phase(
        phase_factory, chapter_factory, phases.CommentPhase,
        module__project__access=Access.SEMIPUBLIC)

    anonymous, moderator, initiator = setup_users(project)
    participant = user_factory()
    project.participants.add(participant)
    group_member_in_orga, group_member_out, group_member_in_project, project \
        = setup_group_users(user_factory, group_factory, project)

    paragraph = paragraph_factory(chapter=item)

    assert project.access == Access.SEMIPUBLIC
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, paragraph)
        assert not rules.has_perm(perm_name, user, paragraph)
        assert not rules.has_perm(perm_name, group_member_in_orga, paragraph)
        assert not rules.has_perm(perm_name, group_member_out, paragraph)
        assert rules.has_perm(perm_name, group_member_in_project, paragraph)
        assert rules.has_perm(perm_name, participant, paragraph)
        assert rules.has_perm(perm_name, moderator, paragraph)
        assert rules.has_perm(perm_name, initiator, paragraph)


@pytest.mark.django_db
def test_phase_active_project_draft(phase_factory, chapter_factory,
                                    paragraph_factory, user_factory,
                                    group_factory, user):
    phase, _, project, item = setup_phase(
        phase_factory, chapter_factory, phases.CommentPhase,
        module__project__is_draft=True)

    anonymous, moderator, initiator = setup_users(project)
    group_member_in_orga, group_member_out, group_member_in_project, project \
        = setup_group_users(user_factory, group_factory, project)

    paragraph = paragraph_factory(chapter=item)

    assert project.is_draft
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, paragraph)
        assert not rules.has_perm(perm_name, user, paragraph)
        assert not rules.has_perm(perm_name, group_member_in_orga, paragraph)
        assert not rules.has_perm(perm_name, group_member_out, paragraph)
        assert rules.has_perm(perm_name, group_member_in_project, paragraph)
        assert rules.has_perm(perm_name, moderator, paragraph)
        assert rules.has_perm(perm_name, initiator, paragraph)


@pytest.mark.django_db
def test_post_phase_project_archived(phase_factory, chapter_factory,
                                     paragraph_factory, user_factory,
                                     group_factory, user):
    phase, _, project, item = setup_phase(phase_factory, chapter_factory,
                                          phases.CommentPhase,
                                          module__project__is_archived=True)

    anonymous, moderator, initiator = setup_users(project)
    group_member_in_orga, group_member_out, group_member_in_project, project \
        = setup_group_users(user_factory, group_factory, project)

    paragraph = paragraph_factory(chapter=item)

    assert project.is_archived
    with freeze_post_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, paragraph)
        assert not rules.has_perm(perm_name, user, paragraph)
        assert not rules.has_perm(perm_name, group_member_in_orga, paragraph)
        assert not rules.has_perm(perm_name, group_member_out, paragraph)
        assert rules.has_perm(perm_name, group_member_in_project, paragraph)
        assert rules.has_perm(perm_name, moderator, paragraph)
        assert rules.has_perm(perm_name, initiator, paragraph)
