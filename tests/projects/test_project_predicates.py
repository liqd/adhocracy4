import pytest
from dateutil.parser import parse
from freezegun import freeze_time

from adhocracy4.projects import predicates
from adhocracy4.projects.enums import Access


@pytest.mark.django_db
def test_is_org_group_member(user_factory, project_factory,
                             group_factory):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()

    group1 = group_factory()
    group2 = group_factory()
    group3 = group_factory()
    group_member_12 = user_factory.create(groups=(group1, group2))
    group_member_23 = user_factory.create(groups=(group2, group3))
    project1 = project_factory(group=group1)
    project2 = project_factory()

    assert not predicates.is_prj_group_member(user, project1)
    assert not predicates.is_prj_group_member(user, project2)
    assert not predicates.is_prj_group_member(user, False)
    assert not predicates.is_prj_group_member(admin, project1)
    assert not predicates.is_prj_group_member(admin, project2)
    assert not predicates.is_prj_group_member(admin, False)
    assert not predicates.is_prj_group_member(initiator, project1)
    assert not predicates.is_prj_group_member(initiator, project2)
    assert not predicates.is_prj_group_member(initiator, False)
    assert predicates.is_prj_group_member(group_member_12, project1)
    assert not predicates.is_prj_group_member(group_member_12, project2)
    assert not predicates.is_prj_group_member(group_member_12, False)
    assert not predicates.is_prj_group_member(group_member_23, project1)
    assert not predicates.is_prj_group_member(group_member_23, project2)
    assert not predicates.is_prj_group_member(group_member_23, False)


@pytest.mark.django_db
def test_is_member(user_factory, project_factory):
    user = user_factory()
    admin = user_factory(is_superuser=True)

    member = user_factory()
    project1 = project_factory(access=Access.PRIVATE)
    project1.participants.add(member)
    project2 = project_factory(access=Access.PRIVATE)
    project3 = project_factory(access=Access.PUBLIC)

    assert not predicates.is_project_member(user, project1)
    assert not predicates.is_project_member(user, project2)
    assert predicates.is_project_member(user, project3)
    assert not predicates.is_project_member(user, False)
    assert not predicates.is_project_member(admin, project1)
    assert not predicates.is_project_member(admin, project2)
    assert predicates.is_project_member(admin, project3)
    assert not predicates.is_project_member(admin, False)
    assert predicates.is_project_member(member, project1)
    assert not predicates.is_project_member(member, project2)
    assert predicates.is_project_member(member, project3)
    assert not predicates.is_project_member(member, False)


@pytest.mark.django_db
def test_is_project_member(user_factory, project_factory):
    user = user_factory()
    admin = user_factory(is_superuser=True)

    member = user_factory()
    project1 = project_factory(access=Access.PRIVATE)
    project1.participants.add(member)
    project2 = project_factory(access=Access.PRIVATE)
    project3 = project_factory(access=Access.PUBLIC)

    assert not predicates.is_project_member(user, project1)
    assert not predicates.is_project_member(user, project2)
    assert predicates.is_project_member(user, project3)
    assert not predicates.is_project_member(user, False)
    assert not predicates.is_project_member(admin, project1)
    assert not predicates.is_project_member(admin, project2)
    assert predicates.is_project_member(admin, project3)
    assert not predicates.is_project_member(admin, False)
    assert predicates.is_project_member(member, project1)
    assert not predicates.is_project_member(member, project2)
    assert predicates.is_project_member(member, project3)
    assert not predicates.is_project_member(member, False)


@pytest.mark.django_db
def test_is_public(user_factory, project_factory):
    user = user_factory()
    admin = user_factory(is_superuser=True)

    project1 = project_factory(access=Access.PRIVATE)
    project2 = project_factory(access=Access.PUBLIC)

    assert not predicates.is_public(user, project1)
    assert predicates.is_public(user, project2)
    assert not predicates.is_public(user, False)
    assert not predicates.is_public(admin, project1)
    assert predicates.is_public(admin, project2)
    assert not predicates.is_public(admin, False)


@pytest.mark.django_db
def test_is_live(user_factory, project_factory):
    user = user_factory()
    admin = user_factory(is_superuser=True)

    project1 = project_factory(is_draft=False)
    project2 = project_factory(is_draft=True)

    assert predicates.is_live(user, project1)
    assert not predicates.is_live(user, project2)
    assert not predicates.is_live(user, False)
    assert predicates.is_live(admin, project1)
    assert not predicates.is_live(admin, project2)
    assert not predicates.is_live(admin, False)


@pytest.mark.django_db
def test_is_moderator(user_factory, project_factory):
    user = user_factory()
    admin = user_factory(is_superuser=True)

    moderator = user_factory()
    project1 = project_factory()
    project1.moderators.add(moderator)
    project2 = project_factory()

    assert not predicates.is_moderator(user, project1)
    assert not predicates.is_moderator(user, project2)
    assert not predicates.is_moderator(user, False)
    assert not predicates.is_moderator(admin, project1)
    assert not predicates.is_moderator(admin, project2)
    assert not predicates.is_moderator(admin, False)
    assert predicates.is_moderator(moderator, project1)
    assert not predicates.is_moderator(moderator, project2)
    assert not predicates.is_moderator(moderator, False)


@pytest.mark.django_db
def test_has_started(user_factory, phase_factory, project_factory):
    user = user_factory()
    admin = user_factory(is_superuser=True)

    project1 = project_factory()
    project2 = project_factory()
    phase_factory(
        start_date=parse('2013-01-01 18:00:00 UTC'),
        end_date=parse('2013-01-02 18:00:00 UTC'),
        module__project=project1,
    )
    phase_factory(
        start_date=parse('2013-02-01 18:00:00 UTC'),
        end_date=parse('2013-02-02 18:00:00 UTC'),
        module__project=project2,
    )

    with freeze_time('2013-01-01 18:30:00 UTC'):
        assert predicates.has_started(user, project1)
        assert not predicates.has_started(user, project2)
        assert not predicates.has_started(user, False)
        assert predicates.has_started(admin, project1)
        assert not predicates.has_started(admin, project2)
        assert not predicates.has_started(admin, False)


@pytest.mark.django_db
def test_has_context_started(user_factory, phase_factory, module_factory,
                             project_factory, question_factory):
    user = user_factory()
    admin = user_factory(is_superuser=True)

    project1 = project_factory()
    project2 = project_factory()
    phase_factory(
        start_date=parse('2013-01-01 18:00:00 UTC'),
        end_date=parse('2013-01-02 18:00:00 UTC'),
        module__project=project1,
    )
    phase_factory(
        start_date=parse('2013-02-01 18:00:00 UTC'),
        end_date=parse('2013-02-02 18:00:00 UTC'),
        module__project=project2,
    )

    question1 = question_factory(module__project=project1)
    question2 = question_factory(module__project=project2)

    with freeze_time('2013-01-01 18:30:00 UTC'):
        assert predicates.has_context_started(user, question1)
        assert not predicates.has_context_started(user, question2)
        assert not predicates.has_context_started(user, False)
        assert predicates.has_context_started(admin, question1)
        assert not predicates.has_context_started(admin, question2)
        assert not predicates.has_context_started(admin, False)
