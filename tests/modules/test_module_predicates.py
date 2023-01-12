import pytest
from dateutil.parser import parse
from freezegun import freeze_time

from adhocracy4.modules import predicates
from adhocracy4.projects.enums import Access


@pytest.mark.django_db
def test_is_context_initiator(
    user_factory,
    question_factory,
    project_factory,
    organisation,
    member_factory,
    group_factory,
):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    moderator = user_factory()
    project_member = user_factory()
    org_member = user_factory()
    group1 = group_factory()
    group_member = user_factory.create(groups=(group1,))

    project = project_factory(
        access=Access.PUBLIC, organisation=organisation, group=group1
    )
    private_project = project_factory(
        access=Access.PRIVATE, organisation=organisation, group=group1
    )
    organisation.initiators.add(initiator)
    private_project.participants.add(project_member)
    private_project.moderators.add(moderator)
    project.moderators.add(moderator)
    member_factory(member=org_member, organisation=organisation)

    question = question_factory(module__project=project)
    question_private = question_factory(module__project=private_project)

    assert not predicates.is_context_initiator(user, project)
    assert not predicates.is_context_initiator(user, private_project)
    assert not predicates.is_context_initiator(user, question)
    assert not predicates.is_context_initiator(user, question_private)
    assert not predicates.is_context_initiator(user, False)
    assert not predicates.is_context_initiator(admin, project)
    assert not predicates.is_context_initiator(admin, private_project)
    assert not predicates.is_context_initiator(admin, question)
    assert not predicates.is_context_initiator(admin, question_private)
    assert not predicates.is_context_initiator(admin, False)
    assert predicates.is_context_initiator(initiator, project)
    assert predicates.is_context_initiator(initiator, private_project)
    assert predicates.is_context_initiator(initiator, question)
    assert predicates.is_context_initiator(initiator, question_private)
    assert not predicates.is_context_initiator(initiator, False)
    assert not predicates.is_context_initiator(moderator, project)
    assert not predicates.is_context_initiator(moderator, private_project)
    assert not predicates.is_context_initiator(moderator, question)
    assert not predicates.is_context_initiator(moderator, question_private)
    assert not predicates.is_context_initiator(moderator, False)
    assert not predicates.is_context_initiator(project_member, project)
    assert not predicates.is_context_initiator(project_member, private_project)
    assert not predicates.is_context_initiator(project_member, question)
    assert not predicates.is_context_initiator(project_member, question_private)
    assert not predicates.is_context_initiator(project_member, False)
    assert not predicates.is_context_initiator(org_member, project)
    assert not predicates.is_context_initiator(org_member, private_project)
    assert not predicates.is_context_initiator(org_member, question)
    assert not predicates.is_context_initiator(org_member, question_private)
    assert not predicates.is_context_initiator(org_member, False)
    assert not predicates.is_context_initiator(group_member, project)
    assert not predicates.is_context_initiator(group_member, private_project)
    assert not predicates.is_context_initiator(group_member, question)
    assert not predicates.is_context_initiator(group_member, question_private)
    assert not predicates.is_context_initiator(group_member, False)


@pytest.mark.django_db
def test_is_context_moderator(
    user_factory,
    question_factory,
    project_factory,
    organisation,
    member_factory,
    group_factory,
):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    moderator = user_factory()
    project_member = user_factory()
    org_member = user_factory()
    group1 = group_factory()
    group_member = user_factory.create(groups=(group1,))

    project = project_factory(
        access=Access.PUBLIC, organisation=organisation, group=group1
    )
    private_project = project_factory(
        access=Access.PRIVATE, organisation=organisation, group=group1
    )
    organisation.initiators.add(initiator)
    private_project.participants.add(project_member)
    private_project.moderators.add(moderator)
    project.moderators.add(moderator)
    member_factory(member=org_member, organisation=organisation)

    question = question_factory(module__project=project)
    question_private = question_factory(module__project=private_project)

    assert not predicates.is_context_moderator(user, project)
    assert not predicates.is_context_moderator(user, private_project)
    assert not predicates.is_context_moderator(user, question)
    assert not predicates.is_context_moderator(user, question_private)
    assert not predicates.is_context_moderator(user, False)
    assert not predicates.is_context_moderator(admin, project)
    assert not predicates.is_context_moderator(admin, private_project)
    assert not predicates.is_context_moderator(admin, question)
    assert not predicates.is_context_moderator(admin, question_private)
    assert not predicates.is_context_moderator(admin, False)
    assert not predicates.is_context_moderator(initiator, project)
    assert not predicates.is_context_moderator(initiator, private_project)
    assert not predicates.is_context_moderator(initiator, question)
    assert not predicates.is_context_moderator(initiator, question_private)
    assert not predicates.is_context_moderator(initiator, False)
    assert predicates.is_context_moderator(moderator, project)
    assert predicates.is_context_moderator(moderator, private_project)
    assert predicates.is_context_moderator(moderator, question)
    assert predicates.is_context_moderator(moderator, question_private)
    assert not predicates.is_context_moderator(moderator, False)
    assert not predicates.is_context_moderator(project_member, project)
    assert not predicates.is_context_moderator(project_member, private_project)
    assert not predicates.is_context_moderator(project_member, question)
    assert not predicates.is_context_moderator(project_member, question_private)
    assert not predicates.is_context_moderator(project_member, False)
    assert not predicates.is_context_moderator(org_member, project)
    assert not predicates.is_context_moderator(org_member, private_project)
    assert not predicates.is_context_moderator(org_member, question)
    assert not predicates.is_context_moderator(org_member, question_private)
    assert not predicates.is_context_moderator(org_member, False)
    assert not predicates.is_context_initiator(group_member, project)
    assert not predicates.is_context_initiator(group_member, private_project)
    assert not predicates.is_context_initiator(group_member, question)
    assert not predicates.is_context_initiator(group_member, question_private)
    assert not predicates.is_context_initiator(group_member, False)


@pytest.mark.django_db
def test_is_context_group_member(
    user_factory,
    question_factory,
    project_factory,
    group_factory,
    organisation,
    member_factory,
):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    moderator = user_factory()
    project_member = user_factory()
    org_member = user_factory()
    group1 = group_factory()
    group_member = user_factory.create(groups=(group1,))

    project = project_factory(
        access=Access.PUBLIC, organisation=organisation, group=group1
    )
    private_project = project_factory(
        access=Access.PRIVATE, organisation=organisation, group=group1
    )
    organisation.initiators.add(initiator)
    private_project.participants.add(project_member)
    private_project.moderators.add(moderator)
    project.moderators.add(moderator)
    member_factory(member=org_member, organisation=organisation)

    question = question_factory(module__project=project)
    question_private = question_factory(module__project=private_project)

    assert not predicates.is_context_group_member(user, project)
    assert not predicates.is_context_group_member(user, private_project)
    assert not predicates.is_context_group_member(user, question_private)
    assert not predicates.is_context_group_member(user, False)
    assert not predicates.is_context_group_member(admin, project)
    assert not predicates.is_context_group_member(admin, private_project)
    assert not predicates.is_context_group_member(admin, question)
    assert not predicates.is_context_group_member(admin, question_private)
    assert not predicates.is_context_group_member(admin, False)
    assert not predicates.is_context_group_member(initiator, project)
    assert not predicates.is_context_group_member(initiator, private_project)
    assert not predicates.is_context_group_member(initiator, question)
    assert not predicates.is_context_group_member(initiator, question_private)
    assert not predicates.is_context_group_member(initiator, False)
    assert not predicates.is_context_group_member(moderator, project)
    assert not predicates.is_context_group_member(moderator, private_project)
    assert not predicates.is_context_group_member(moderator, question)
    assert not predicates.is_context_group_member(moderator, question_private)
    assert not predicates.is_context_group_member(moderator, False)
    assert not predicates.is_context_group_member(project_member, project)
    assert not predicates.is_context_group_member(project_member, private_project)
    assert not predicates.is_context_group_member(project_member, question)
    assert not predicates.is_context_group_member(project_member, question_private)
    assert not predicates.is_context_group_member(project_member, False)
    assert not predicates.is_context_group_member(org_member, project)
    assert not predicates.is_context_group_member(org_member, private_project)
    assert not predicates.is_context_group_member(org_member, question)
    assert not predicates.is_context_group_member(org_member, question_private)
    assert not predicates.is_context_group_member(org_member, False)
    assert predicates.is_context_group_member(group_member, project)
    assert predicates.is_context_group_member(group_member, private_project)
    assert predicates.is_context_group_member(group_member, question)
    assert predicates.is_context_group_member(group_member, question_private)
    assert not predicates.is_context_group_member(group_member, False)


@pytest.mark.django_db
def test_is_context_member(
    user_factory,
    question_factory,
    project_factory,
    organisation,
    member_factory,
    group_factory,
):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    moderator = user_factory()
    project_member = user_factory()
    org_member = user_factory()
    group1 = group_factory()
    group_member = user_factory.create(groups=(group1,))

    project = project_factory(
        access=Access.PUBLIC, organisation=organisation, group=group1
    )
    private_project = project_factory(
        access=Access.PRIVATE, organisation=organisation, group=group1
    )
    organisation.initiators.add(initiator)
    private_project.participants.add(project_member)
    private_project.moderators.add(moderator)
    project.moderators.add(moderator)
    member_factory(member=org_member, organisation=organisation)

    question = question_factory(module__project=project)
    question_private = question_factory(module__project=private_project)

    assert predicates.is_context_member(user, question)
    assert not predicates.is_context_member(user, question_private)
    assert not predicates.is_context_member(user, False)
    assert predicates.is_context_member(admin, question)
    assert not predicates.is_context_member(admin, question_private)
    assert not predicates.is_context_member(admin, False)
    assert predicates.is_context_member(initiator, question)
    assert not predicates.is_context_member(initiator, question_private)
    assert not predicates.is_context_member(initiator, False)
    assert predicates.is_context_member(moderator, question)
    assert predicates.is_context_member(moderator, question_private)
    assert not predicates.is_context_member(moderator, False)
    assert predicates.is_context_member(project_member, question)
    assert predicates.is_context_member(project_member, question_private)
    assert not predicates.is_context_member(project_member, False)
    assert predicates.is_context_member(org_member, question)
    assert predicates.is_context_member(org_member, question_private)
    assert not predicates.is_context_member(org_member, False)
    assert predicates.is_context_member(group_member, question)
    assert not predicates.is_context_member(group_member, question_private)
    assert not predicates.is_context_member(group_member, False)


@pytest.mark.django_db
def test_is_owner(user_factory, question_factory, project_factory, organisation):
    user = user_factory()
    owner = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    moderator = user_factory()

    project = project_factory(organisation=organisation)
    organisation.initiators.add(initiator)
    project.moderators.add(moderator)

    question = question_factory(creator=owner, module__project=project)

    assert not predicates.is_owner(user, question)
    assert not predicates.is_owner(user, False)
    assert predicates.is_owner(owner, question)
    assert not predicates.is_owner(owner, False)
    assert not predicates.is_owner(admin, question)
    assert not predicates.is_owner(admin, False)
    assert not predicates.is_owner(initiator, question)
    assert not predicates.is_owner(initiator, False)
    assert not predicates.is_owner(moderator, question)
    assert not predicates.is_owner(moderator, False)


@pytest.mark.django_db
def test_is_public_context(
    user_factory, question_factory, project_factory, organisation, member_factory
):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    moderator = user_factory()
    org_member = user_factory()

    project = project_factory(is_draft=False, organisation=organisation)
    draft_project = project_factory(
        is_draft=True, access=Access.PUBLIC, organisation=organisation
    )
    semipublic_project = project_factory(
        is_draft=False, access=Access.SEMIPUBLIC, organisation=organisation
    )
    private_project = project_factory(
        is_draft=False, access=Access.PRIVATE, organisation=organisation
    )
    organisation.initiators.add(initiator)
    draft_project.moderators.add(moderator)
    project.moderators.add(moderator)
    member_factory(member=org_member, organisation=organisation)

    question = question_factory(module__project=project)
    question_draft = question_factory(module__project=draft_project)
    question_semipublic = question_factory(module__project=semipublic_project)
    question_private = question_factory(module__project=private_project)

    assert predicates.is_public_context(user, question)
    assert predicates.is_public_context(user, question_draft)
    assert predicates.is_public_context(user, question_semipublic)
    assert not predicates.is_public_context(user, question_private)
    assert not predicates.is_public_context(user, False)
    assert predicates.is_public_context(admin, question)
    assert predicates.is_public_context(admin, question_draft)
    assert predicates.is_public_context(admin, question_semipublic)
    assert not predicates.is_public_context(admin, question_private)
    assert not predicates.is_public_context(admin, False)
    assert predicates.is_public_context(initiator, question)
    assert predicates.is_public_context(initiator, question_draft)
    assert predicates.is_public_context(initiator, question_semipublic)
    assert not predicates.is_public_context(initiator, question_private)
    assert not predicates.is_public_context(initiator, False)
    assert predicates.is_public_context(moderator, question)
    assert predicates.is_public_context(moderator, question_draft)
    assert predicates.is_public_context(moderator, question_semipublic)
    assert not predicates.is_public_context(moderator, question_private)
    assert not predicates.is_public_context(moderator, False)
    assert predicates.is_public_context(org_member, question)
    assert predicates.is_public_context(org_member, question_draft)
    assert predicates.is_public_context(org_member, question_semipublic)
    assert not predicates.is_public_context(org_member, question_private)
    assert not predicates.is_public_context(org_member, False)


@pytest.mark.django_db
def test_is_live_context(
    user_factory, question_factory, project_factory, organisation, member_factory
):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    moderator = user_factory()
    org_member = user_factory()

    project = project_factory(is_draft=False, organisation=organisation)
    draft_project = project_factory(is_draft=True, organisation=organisation)
    organisation.initiators.add(initiator)
    draft_project.moderators.add(moderator)
    project.moderators.add(moderator)
    member_factory(member=org_member, organisation=organisation)

    question = question_factory(module__project=project)
    question_draft = question_factory(module__project=draft_project)

    assert predicates.is_live_context(user, question)
    assert not predicates.is_live_context(user, question_draft)
    assert not predicates.is_live_context(user, False)
    assert predicates.is_live_context(admin, question)
    assert not predicates.is_live_context(admin, question_draft)
    assert not predicates.is_live_context(admin, False)
    assert predicates.is_live_context(initiator, question)
    assert not predicates.is_live_context(initiator, question_draft)
    assert not predicates.is_live_context(initiator, False)
    assert predicates.is_live_context(moderator, question)
    assert not predicates.is_live_context(moderator, question_draft)
    assert not predicates.is_live_context(moderator, False)
    assert predicates.is_live_context(org_member, question)
    assert not predicates.is_live_context(org_member, question_draft)
    assert not predicates.is_live_context(org_member, False)


@pytest.mark.django_db
def test_is_allowed_moderate_project(
    user_factory,
    question_factory,
    project_factory,
    group_factory,
    organisation,
    member_factory,
):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    moderator = user_factory()
    project_member = user_factory()
    org_member = user_factory()
    group1 = group_factory()
    group2 = group_factory()
    group_member = user_factory.create(groups=(group1,))

    project = project_factory(
        access=Access.PUBLIC, organisation=organisation, group=group2
    )
    private_project = project_factory(
        access=Access.PRIVATE, organisation=organisation, group=group1
    )
    organisation.initiators.add(initiator)
    private_project.participants.add(project_member)
    private_project.moderators.add(moderator)
    project.moderators.add(moderator)
    member_factory(member=org_member, organisation=organisation)

    question = question_factory(module__project=project)
    question_private = question_factory(module__project=private_project)

    assert not predicates.is_allowed_moderate_project(user, project)
    assert not predicates.is_allowed_moderate_project(user, private_project)
    assert not predicates.is_allowed_moderate_project(user, question)
    assert not predicates.is_allowed_moderate_project(user, question_private)
    assert not predicates.is_allowed_moderate_project(user, False)

    assert predicates.is_allowed_moderate_project(admin, project)
    assert predicates.is_allowed_moderate_project(admin, private_project)
    assert predicates.is_allowed_moderate_project(admin, question)
    assert predicates.is_allowed_moderate_project(admin, question_private)
    assert not predicates.is_allowed_moderate_project(admin, False)

    assert predicates.is_allowed_moderate_project(initiator, project)
    assert predicates.is_allowed_moderate_project(initiator, private_project)
    assert predicates.is_allowed_moderate_project(initiator, question)
    assert predicates.is_allowed_moderate_project(initiator, question_private)
    assert not predicates.is_allowed_moderate_project(initiator, False)

    assert predicates.is_allowed_moderate_project(moderator, project)
    assert predicates.is_allowed_moderate_project(moderator, private_project)
    assert predicates.is_allowed_moderate_project(moderator, question)
    assert predicates.is_allowed_moderate_project(moderator, question_private)
    assert not predicates.is_allowed_moderate_project(moderator, False)

    assert not predicates.is_allowed_moderate_project(project_member, project)
    assert not predicates.is_allowed_moderate_project(project_member, private_project)
    assert not predicates.is_allowed_moderate_project(project_member, question)
    assert not predicates.is_allowed_moderate_project(project_member, question_private)
    assert not predicates.is_allowed_moderate_project(project_member, False)

    assert not predicates.is_allowed_moderate_project(org_member, project)
    assert not predicates.is_allowed_moderate_project(org_member, private_project)
    assert not predicates.is_allowed_moderate_project(org_member, question)
    assert not predicates.is_allowed_moderate_project(org_member, question_private)
    assert not predicates.is_allowed_moderate_project(org_member, False)

    assert not predicates.is_allowed_moderate_project(group_member, project)
    assert predicates.is_allowed_moderate_project(group_member, private_project)
    assert not predicates.is_allowed_moderate_project(group_member, question)
    assert predicates.is_allowed_moderate_project(group_member, question_private)
    assert not predicates.is_allowed_moderate_project(group_member, False)


@pytest.mark.django_db
def test_is_allowed_crud_project(
    user_factory,
    question_factory,
    project_factory,
    group_factory,
    organisation,
    member_factory,
):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    moderator = user_factory()
    project_member = user_factory()
    org_member = user_factory()
    group1 = group_factory()
    group_member = user_factory.create(groups=(group1,))

    project = project_factory(
        access=Access.PUBLIC, organisation=organisation, group=group1
    )
    private_project = project_factory(
        access=Access.PRIVATE, organisation=organisation, group=group1
    )
    organisation.initiators.add(initiator)
    private_project.participants.add(project_member)
    private_project.moderators.add(moderator)
    project.moderators.add(moderator)
    member_factory(member=org_member, organisation=organisation)

    question = question_factory(module__project=project)
    question_private = question_factory(module__project=private_project)

    assert not predicates.is_allowed_crud_project(user, question)
    assert not predicates.is_allowed_crud_project(user, question_private)
    assert not predicates.is_allowed_crud_project(user, False)
    assert predicates.is_allowed_crud_project(admin, question)
    assert predicates.is_allowed_crud_project(admin, question_private)
    assert not predicates.is_allowed_crud_project(admin, False)
    assert predicates.is_allowed_crud_project(initiator, question)
    assert predicates.is_allowed_crud_project(initiator, question_private)
    assert not predicates.is_allowed_crud_project(initiator, False)
    assert not predicates.is_allowed_crud_project(moderator, question)
    assert not predicates.is_allowed_crud_project(moderator, question_private)
    assert not predicates.is_allowed_crud_project(moderator, False)
    assert not predicates.is_allowed_crud_project(project_member, question)
    assert not predicates.is_allowed_crud_project(project_member, question_private)
    assert not predicates.is_allowed_crud_project(project_member, False)
    assert not predicates.is_allowed_crud_project(org_member, question)
    assert not predicates.is_allowed_crud_project(org_member, question_private)
    assert not predicates.is_allowed_crud_project(org_member, False)
    assert predicates.is_allowed_crud_project(group_member, question)
    assert predicates.is_allowed_crud_project(group_member, question_private)
    assert not predicates.is_allowed_crud_project(group_member, False)


@pytest.mark.django_db
def test_is_project_admin(
    user_factory,
    question_factory,
    project_factory,
    organisation,
    member_factory,
    group_factory,
):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    moderator = user_factory()
    project_member = user_factory()
    org_member = user_factory()
    group1 = group_factory()
    group_member = user_factory.create(groups=(group1,))

    project = project_factory(
        access=Access.PUBLIC, organisation=organisation, group=group1
    )
    private_project = project_factory(
        access=Access.PRIVATE, organisation=organisation, group=group1
    )
    organisation.initiators.add(initiator)
    private_project.participants.add(project_member)
    private_project.moderators.add(moderator)
    project.moderators.add(moderator)
    member_factory(member=org_member, organisation=organisation)

    question = question_factory(module__project=project)
    question_private = question_factory(module__project=private_project)

    assert not predicates.is_project_admin(user, question)
    assert not predicates.is_project_admin(user, question_private)
    assert not predicates.is_project_admin(user, False)
    assert predicates.is_project_admin(admin, question)
    assert predicates.is_project_admin(admin, question_private)
    assert not predicates.is_project_admin(admin, False)
    assert predicates.is_project_admin(initiator, question)
    assert predicates.is_project_admin(initiator, question_private)
    assert not predicates.is_project_admin(initiator, False)
    assert predicates.is_project_admin(moderator, question)
    assert predicates.is_project_admin(moderator, question_private)
    assert not predicates.is_project_admin(moderator, False)
    assert not predicates.is_project_admin(project_member, question)
    assert not predicates.is_project_admin(project_member, question_private)
    assert not predicates.is_project_admin(project_member, False)
    assert not predicates.is_project_admin(org_member, question)
    assert not predicates.is_project_admin(org_member, question_private)
    assert not predicates.is_project_admin(org_member, False)
    assert predicates.is_project_admin(group_member, question)
    assert predicates.is_project_admin(group_member, question_private)
    assert not predicates.is_project_admin(group_member, False)


@pytest.mark.django_db
def test_is_allowed_view_item(
    user_factory,
    question_factory,
    project_factory,
    organisation,
    member_factory,
    group_factory,
):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    moderator = user_factory()
    project_member = user_factory()
    org_member = user_factory()
    group1 = group_factory()
    group_member = user_factory.create(groups=(group1,))

    project = project_factory(
        access=Access.PUBLIC, organisation=organisation, group=group1
    )
    private_project = project_factory(
        access=Access.PRIVATE, organisation=organisation, group=group1
    )
    organisation.initiators.add(initiator)
    private_project.participants.add(project_member)
    private_project.moderators.add(moderator)
    project.moderators.add(moderator)
    member_factory(member=org_member, organisation=organisation)

    question = question_factory(module__project=project)
    question_private = question_factory(module__project=private_project)

    assert predicates.is_allowed_view_item(user, question)
    assert not predicates.is_allowed_view_item(user, question_private)
    assert not predicates.is_allowed_view_item(user, False)
    assert predicates.is_allowed_view_item(admin, question)
    assert predicates.is_allowed_view_item(admin, question_private)
    assert not predicates.is_allowed_view_item(admin, False)
    assert predicates.is_allowed_view_item(initiator, question)
    assert predicates.is_allowed_view_item(initiator, question_private)
    assert not predicates.is_allowed_view_item(initiator, False)
    assert predicates.is_allowed_view_item(moderator, question)
    assert predicates.is_allowed_view_item(moderator, question_private)
    assert not predicates.is_allowed_view_item(moderator, False)
    assert predicates.is_allowed_view_item(project_member, question)
    assert predicates.is_allowed_view_item(project_member, question_private)
    assert not predicates.is_allowed_view_item(project_member, False)
    assert predicates.is_allowed_view_item(org_member, question)
    assert predicates.is_allowed_view_item(org_member, question_private)
    assert not predicates.is_allowed_view_item(org_member, False)
    assert predicates.is_allowed_view_item(group_member, question)
    assert predicates.is_allowed_view_item(group_member, question_private)
    assert not predicates.is_allowed_view_item(group_member, False)


@pytest.mark.django_db
def test_module_is_between_phases(module, phase_factory):
    phase1 = phase_factory(
        start_date=parse("2022-01-01 16:00:00 UTC"),
        end_date=parse("2022-01-01 18:00:00 UTC"),
        type="phase_content_factory:first_phase",
        module=module,
    )
    phase2 = phase_factory(
        start_date=parse("2022-01-01 20:00:00 UTC"),
        end_date=parse("2022-01-01 22:00:00 UTC"),
        type="phase_content_factory:second_phase",
        module=module,
    )

    with freeze_time("2022-01-01 15:00:00 UTC"):
        assert not predicates.module_is_between_phases(phase1.type, phase2.type, module)
    with freeze_time("2022-01-01 17:00:00 UTC"):
        assert not predicates.module_is_between_phases(phase1.type, phase2.type, module)
    with freeze_time("2022-01-01 19:00:00 UTC"):
        assert predicates.module_is_between_phases(phase1.type, phase2.type, module)
    with freeze_time("2022-01-01 21:00:00 UTC"):
        assert not predicates.module_is_between_phases(phase1.type, phase2.type, module)
    with freeze_time("2022-01-01 23:00:00 UTC"):
        assert not predicates.module_is_between_phases(phase1.type, phase2.type, module)
