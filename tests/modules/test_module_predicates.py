import pytest

from adhocracy4.modules import predicates
from adhocracy4.projects.enums import Access


@pytest.mark.django_db
def test_is_context_initiator(user_factory, question_factory, project_factory,
                              organisation, member_factory):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    moderator = user_factory()
    project_member = user_factory()
    org_member = user_factory()

    project = project_factory(access=Access.PUBLIC, organisation=organisation)
    private_project = project_factory(access=Access.PRIVATE,
                                      organisation=organisation)
    organisation.initiators.add(initiator)
    private_project.participants.add(project_member)
    private_project.moderators.add(moderator)
    project.moderators.add(moderator)
    member_factory(member=org_member, organisation=organisation)

    question = question_factory(module__project=project)
    question_private = question_factory(module__project=private_project)

    assert not predicates.is_context_initiator(user, question)
    assert not predicates.is_context_initiator(user, question_private)
    assert not predicates.is_context_initiator(user, False)
    assert not predicates.is_context_initiator(admin, question)
    assert not predicates.is_context_initiator(admin, question_private)
    assert not predicates.is_context_initiator(admin, False)
    assert predicates.is_context_initiator(initiator, question)
    assert predicates.is_context_initiator(initiator, question_private)
    assert not predicates.is_context_initiator(initiator, False)
    assert not predicates.is_context_initiator(moderator, question)
    assert not predicates.is_context_initiator(moderator, question_private)
    assert not predicates.is_context_initiator(moderator, False)
    assert not predicates.is_context_initiator(project_member, question)
    assert not predicates.is_context_initiator(project_member,
                                               question_private)
    assert not predicates.is_context_initiator(project_member, False)
    assert not predicates.is_context_initiator(org_member, question)
    assert not predicates.is_context_initiator(org_member, question_private)
    assert not predicates.is_context_initiator(org_member, False)


@pytest.mark.django_db
def test_is_context_moderator(user_factory, question_factory, project_factory,
                              organisation, member_factory):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    moderator = user_factory()
    project_member = user_factory()
    org_member = user_factory()

    project = project_factory(access=Access.PUBLIC, organisation=organisation)
    private_project = project_factory(access=Access.PRIVATE,
                                      organisation=organisation)
    organisation.initiators.add(initiator)
    private_project.participants.add(project_member)
    private_project.moderators.add(moderator)
    project.moderators.add(moderator)
    member_factory(member=org_member, organisation=organisation)

    question = question_factory(module__project=project)
    question_private = question_factory(module__project=private_project)

    assert not predicates.is_context_moderator(user, question)
    assert not predicates.is_context_moderator(user, question_private)
    assert not predicates.is_context_moderator(user, False)
    assert not predicates.is_context_moderator(admin, question)
    assert not predicates.is_context_moderator(admin, question_private)
    assert not predicates.is_context_moderator(admin, False)
    assert not predicates.is_context_moderator(initiator, question)
    assert not predicates.is_context_moderator(initiator, question_private)
    assert not predicates.is_context_moderator(initiator, False)
    assert predicates.is_context_moderator(moderator, question)
    assert predicates.is_context_moderator(moderator, question_private)
    assert not predicates.is_context_moderator(moderator, False)
    assert not predicates.is_context_moderator(project_member, question)
    assert not predicates.is_context_moderator(project_member,
                                               question_private)
    assert not predicates.is_context_moderator(project_member, False)
    assert not predicates.is_context_moderator(org_member, question)
    assert not predicates.is_context_moderator(org_member, question_private)
    assert not predicates.is_context_moderator(org_member, False)


@pytest.mark.django_db
def test_is_context_member(user_factory, question_factory, project_factory,
                           organisation, member_factory):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    moderator = user_factory()
    project_member = user_factory()
    org_member = user_factory()

    project = project_factory(access=Access.PUBLIC, organisation=organisation)
    private_project = project_factory(access=Access.PRIVATE,
                                      organisation=organisation)
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


@pytest.mark.django_db
def test_is_owner(user_factory, question_factory, project_factory,
                  organisation):
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
def test_is_live_context(user_factory, question_factory, project_factory,
                         organisation, member_factory):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    moderator = user_factory()
    org_member = user_factory()

    project = project_factory(is_draft=False, organisation=organisation)
    draft_project = project_factory(is_draft=True,
                                    organisation=organisation)
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
def test_is_project_admin(user_factory, question_factory, project_factory,
                          organisation, member_factory):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    moderator = user_factory()
    project_member = user_factory()
    org_member = user_factory()

    project = project_factory(access=Access.PUBLIC, organisation=organisation)
    private_project = project_factory(access=Access.PRIVATE,
                                      organisation=organisation)
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


@pytest.mark.django_db
def test_is_allowed_view_item(user_factory, question_factory, project_factory,
                              organisation, member_factory):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    moderator = user_factory()
    project_member = user_factory()
    org_member = user_factory()

    project = project_factory(access=Access.PUBLIC, organisation=organisation)
    private_project = project_factory(access=Access.PRIVATE,
                                      organisation=organisation)
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
