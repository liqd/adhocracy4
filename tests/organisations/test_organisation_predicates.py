import pytest

from adhocracy4.organisations import predicates


@pytest.mark.django_db
def test_is_initiator(user_factory, organisation_factory,
                      project_factory):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator1 = user_factory()
    initiator2 = user_factory()

    organisation1 = organisation_factory()
    organisation1.initiators.add(initiator1)
    organisation2 = organisation_factory()
    organisation2.initiators.add(initiator1, initiator2)
    project1 = project_factory(organisation=organisation1)
    project2 = project_factory(organisation=organisation2)

    assert not predicates.is_initiator(user, organisation1)
    assert not predicates.is_initiator(user, organisation2)
    assert not predicates.is_initiator(user, project1)
    assert not predicates.is_initiator(user, project2)
    assert not predicates.is_initiator(user, False)
    assert not predicates.is_initiator(admin, organisation1)
    assert not predicates.is_initiator(admin, organisation2)
    assert not predicates.is_initiator(admin, project1)
    assert not predicates.is_initiator(admin, project2)
    assert not predicates.is_initiator(admin, False)
    assert predicates.is_initiator(initiator1, organisation1)
    assert predicates.is_initiator(initiator1, organisation2)
    assert predicates.is_initiator(initiator1, project1)
    assert predicates.is_initiator(initiator1, project2)
    assert not predicates.is_initiator(initiator1, False)
    assert not predicates.is_initiator(initiator2, organisation1)
    assert predicates.is_initiator(initiator2, organisation2)
    assert not predicates.is_initiator(initiator2, project1)
    assert predicates.is_initiator(initiator2, project2)
    assert not predicates.is_initiator(initiator2, False)


@pytest.mark.django_db
def test_is_org_member(user_factory, organisation_factory,
                       project_factory, member_factory):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    member1 = user_factory()
    member2 = user_factory()

    organisation1 = organisation_factory()
    member_factory(member=member1, organisation=organisation1)
    organisation2 = organisation_factory()
    member_factory(member=member1, organisation=organisation2)
    member_factory(member=member2, organisation=organisation2)
    project1 = project_factory(organisation=organisation1)
    project2 = project_factory(organisation=organisation2)

    assert not predicates.is_org_member(user, organisation1)
    assert not predicates.is_org_member(user, organisation2)
    assert not predicates.is_org_member(user, project1)
    assert not predicates.is_org_member(user, project2)
    assert not predicates.is_org_member(user, False)
    assert not predicates.is_org_member(admin, organisation1)
    assert not predicates.is_org_member(admin, organisation2)
    assert not predicates.is_org_member(admin, project1)
    assert not predicates.is_org_member(admin, project2)
    assert not predicates.is_org_member(admin, False)
    assert predicates.is_org_member(member1, organisation1)
    assert predicates.is_org_member(member1, organisation2)
    assert predicates.is_org_member(member1, project1)
    assert predicates.is_org_member(member1, project2)
    assert not predicates.is_org_member(member1, False)
    assert not predicates.is_org_member(member2, organisation1)
    assert predicates.is_org_member(member2, organisation2)
    assert not predicates.is_org_member(member2, project1)
    assert predicates.is_org_member(member2, project2)
    assert not predicates.is_org_member(member2, False)


@pytest.mark.django_db
def test_is_org_group_member(user_factory, organisation_factory,
                             project_factory, group_factory):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()

    group1 = group_factory()
    group2 = group_factory()
    group3 = group_factory()
    group_member_12 = user_factory.create(groups=(group1, group2))
    group_member_23 = user_factory.create(groups=(group2, group3))

    organisation1 = organisation_factory()
    organisation1.initiators.add(initiator)
    organisation1.groups.add(group1)
    organisation2 = organisation_factory()
    organisation2.groups.add(group2)
    project1 = project_factory(organisation=organisation1)
    project2 = project_factory(organisation=organisation2)

    assert not predicates.is_org_group_member(user, organisation1)
    assert not predicates.is_org_group_member(user, organisation2)
    assert not predicates.is_org_group_member(user, project1)
    assert not predicates.is_org_group_member(user, project2)
    assert not predicates.is_org_group_member(user, False)
    assert not predicates.is_org_group_member(admin, organisation1)
    assert not predicates.is_org_group_member(admin, organisation2)
    assert not predicates.is_org_group_member(admin, project1)
    assert not predicates.is_org_group_member(admin, project2)
    assert not predicates.is_org_group_member(admin, False)
    assert not predicates.is_org_group_member(initiator, organisation1)
    assert not predicates.is_org_group_member(initiator, organisation2)
    assert not predicates.is_org_group_member(initiator, project1)
    assert not predicates.is_org_group_member(initiator, project2)
    assert not predicates.is_org_group_member(initiator, False)
    assert predicates.is_org_group_member(group_member_12, organisation1)
    assert predicates.is_org_group_member(group_member_12, organisation2)
    assert predicates.is_org_group_member(group_member_12, project1)
    assert predicates.is_org_group_member(group_member_12, project2)
    assert not predicates.is_org_group_member(group_member_12, False)
    assert not predicates.is_org_group_member(group_member_23, organisation1)
    assert predicates.is_org_group_member(group_member_23, organisation2)
    assert not predicates.is_org_group_member(group_member_23, project1)
    assert predicates.is_org_group_member(group_member_23, project2)
    assert not predicates.is_org_group_member(group_member_23, False)
