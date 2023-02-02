import pytest
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils import translation
from rest_framework import status

from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.budgeting import phases
from meinberlin.apps.votes.models import TokenVote


def add_token_to_session(session, token):
    if "voting_tokens" in session:
        session["voting_tokens"][str(token.module.id)] = token.token_hash
    else:
        session["voting_tokens"] = {str(token.module.id): token.token_hash}
    session.save()


@pytest.mark.django_db
def test_voting_phase_active_valid_token_anonymous_can_vote(
    apiclient, voting_token_factory, phase_factory, proposal_factory
):

    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    proposal_ct = ContentType.objects.get_for_model(proposal.__class__)
    token = voting_token_factory(module=module)

    add_token_to_session(apiclient.session, token)

    url = reverse(
        "tokenvotes-list",
        kwargs={"module_pk": module.pk, "content_type": proposal_ct.id},
    )

    data = {"object_id": proposal.pk}

    with freeze_phase(phase):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert TokenVote.objects.all().count() == 1


@pytest.mark.django_db
def test_voting_phase_active_valid_token_user_can_vote(
    apiclient, user, voting_token_factory, phase_factory, proposal_factory
):

    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    proposal_ct = ContentType.objects.get_for_model(proposal.__class__)
    token = voting_token_factory(module=module)

    add_token_to_session(apiclient.session, token)

    url = reverse(
        "tokenvotes-list",
        kwargs={"module_pk": module.pk, "content_type": proposal_ct.id},
    )

    data = {"object_id": proposal.pk}

    with freeze_phase(phase):
        assert apiclient.login(username=user.email, password="password")
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert TokenVote.objects.all().count() == 1


@pytest.mark.django_db
def test_voting_phase_active_valid_token_admin_can_vote(
    apiclient, admin, voting_token_factory, phase_factory, proposal_factory
):

    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    proposal_ct = ContentType.objects.get_for_model(proposal.__class__)
    token = voting_token_factory(module=module)

    add_token_to_session(apiclient.session, token)

    url = reverse(
        "tokenvotes-list",
        kwargs={"module_pk": module.pk, "content_type": proposal_ct.id},
    )
    data = {"object_id": proposal.pk}

    with freeze_phase(phase):
        assert apiclient.login(username=admin.email, password="password")
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert TokenVote.objects.all().count() == 1


@pytest.mark.django_db
def test_voting_phase_inactive_valid_token_anonymous_cannot_vote(
    apiclient, voting_token_factory, phase_factory, proposal_factory
):

    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.CollectPhase
    )
    proposal_ct = ContentType.objects.get_for_model(proposal.__class__)
    token = voting_token_factory(module=module)

    url = reverse(
        "tokenvotes-list",
        kwargs={"module_pk": module.pk, "content_type": proposal_ct.id},
    )
    data = {"object_id": proposal.pk}
    add_token_to_session(apiclient.session, token)

    with freeze_phase(phase):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert TokenVote.objects.all().count() == 0


@pytest.mark.django_db
def test_voting_phase_inactive_valid_token_user_cannot_vote(
    apiclient, user, voting_token_factory, phase_factory, proposal_factory
):

    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.CollectPhase
    )
    proposal_ct = ContentType.objects.get_for_model(proposal.__class__)
    token = voting_token_factory(module=module)

    url = reverse(
        "tokenvotes-list",
        kwargs={"module_pk": module.pk, "content_type": proposal_ct.id},
    )
    data = {"object_id": proposal.pk}
    add_token_to_session(apiclient.session, token)

    with freeze_phase(phase):
        assert apiclient.login(username=user.email, password="password")
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert TokenVote.objects.all().count() == 0


@pytest.mark.django_db
def test_voting_phase_inactive_valid_token_admin_can_vote(
    apiclient, admin, voting_token_factory, phase_factory, proposal_factory
):

    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.CollectPhase
    )
    proposal_ct = ContentType.objects.get_for_model(proposal.__class__)
    token = voting_token_factory(module=module)

    url = reverse(
        "tokenvotes-list",
        kwargs={"module_pk": module.pk, "content_type": proposal_ct.id},
    )
    data = {"object_id": proposal.pk}
    add_token_to_session(apiclient.session, token)

    with freeze_phase(phase):
        assert apiclient.login(username=admin.email, password="password")
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert TokenVote.objects.all().count() == 1


@pytest.mark.django_db
def test_voting_phase_active_valid_token_anonymous_cannot_vote_on_archived(
    apiclient, voting_token_factory, phase_factory, proposal_factory
):

    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    proposal_ct = ContentType.objects.get_for_model(proposal.__class__)

    proposal.is_archived = True
    proposal.save()

    token = voting_token_factory(module=module)

    url = reverse(
        "tokenvotes-list",
        kwargs={"module_pk": module.pk, "content_type": proposal_ct.id},
    )
    data = {"object_id": proposal.pk}
    add_token_to_session(apiclient.session, token)

    with freeze_phase(phase):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert TokenVote.objects.all().count() == 0


@pytest.mark.django_db
def test_voting_phase_active_valid_token_user_cannot_vote_on_archived(
    apiclient, user, voting_token_factory, phase_factory, proposal_factory
):

    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    proposal_ct = ContentType.objects.get_for_model(proposal.__class__)

    proposal.is_archived = True
    proposal.save()

    token = voting_token_factory(module=module)

    url = reverse(
        "tokenvotes-list",
        kwargs={"module_pk": module.pk, "content_type": proposal_ct.id},
    )
    data = {"object_id": proposal.pk}
    add_token_to_session(apiclient.session, token)

    with freeze_phase(phase):
        assert apiclient.login(username=user.email, password="password")
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert TokenVote.objects.all().count() == 0


@pytest.mark.django_db
def test_voting_phase_active_valid_token_admin_can_vote_on_archived(
    apiclient, admin, voting_token_factory, phase_factory, proposal_factory
):

    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    proposal_ct = ContentType.objects.get_for_model(proposal.__class__)

    proposal.is_archived = True
    proposal.save()

    token = voting_token_factory(module=module)

    url = reverse(
        "tokenvotes-list",
        kwargs={"module_pk": module.pk, "content_type": proposal_ct.id},
    )
    data = {"object_id": proposal.pk}
    add_token_to_session(apiclient.session, token)

    with freeze_phase(phase):
        assert apiclient.login(username=admin.email, password="password")
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert TokenVote.objects.all().count() == 1


@pytest.mark.django_db
def test_voting_phase_active_no_token(
    apiclient,
    admin,
    phase_factory,
    proposal_factory,
):

    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    proposal_ct = ContentType.objects.get_for_model(proposal.__class__)

    url = reverse(
        "tokenvotes-list",
        kwargs={"module_pk": module.pk, "content_type": proposal_ct.id},
    )
    data = {"object_id": proposal.pk}

    with freeze_phase(phase):
        with translation.override("en_GB"):
            assert apiclient.login(username=admin.email, password="password")
            response = apiclient.post(url, data, format="json")
            assert response.status_code == status.HTTP_403_FORBIDDEN
            assert (
                "No token given or token not valid for module."
                in response.content.decode()
            )
            assert TokenVote.objects.all().count() == 0


@pytest.mark.django_db
def test_voting_phase_active_token_wrong_module(
    apiclient,
    admin,
    voting_token_factory,
    phase_factory,
    proposal_factory,
    module_factory,
):

    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    proposal_ct = ContentType.objects.get_for_model(proposal.__class__)
    other_module = module_factory()
    token = voting_token_factory(module=other_module)

    url = reverse(
        "tokenvotes-list",
        kwargs={"module_pk": module.pk, "content_type": proposal_ct.id},
    )
    data = {"object_id": proposal.pk}
    add_token_to_session(apiclient.session, token)

    with freeze_phase(phase):
        with translation.override("en_GB"):
            assert apiclient.login(username=admin.email, password="password")
            response = apiclient.post(url, data, format="json")
            assert response.status_code == status.HTTP_403_FORBIDDEN
            assert (
                "No token given or token not valid for module."
                in response.content.decode()
            )
            assert TokenVote.objects.all().count() == 0


@pytest.mark.django_db
def test_voting_phase_active_token_inactive(
    apiclient,
    admin,
    voting_token_factory,
    phase_factory,
    proposal_factory,
):

    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    proposal_ct = ContentType.objects.get_for_model(proposal.__class__)
    token = voting_token_factory(module=module, is_active=False)

    url = reverse(
        "tokenvotes-list",
        kwargs={"module_pk": module.pk, "content_type": proposal_ct.id},
    )
    data = {"object_id": proposal.pk}
    add_token_to_session(apiclient.session, token)

    with freeze_phase(phase):
        with translation.override("en_GB"):
            assert apiclient.login(username=admin.email, password="password")
            response = apiclient.post(url, data, format="json")
            assert response.status_code == status.HTTP_403_FORBIDDEN
            assert "Token is inactive." in response.content.decode()
            assert TokenVote.objects.all().count() == 0


@pytest.mark.django_db
def test_voting_phase_active_token_no_votes_left(
    apiclient,
    admin,
    token_vote_factory,
    voting_token_factory,
    phase_factory,
    proposal_factory,
):

    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    proposal_ct = ContentType.objects.get_for_model(proposal.__class__)
    token = voting_token_factory(module=module)

    for i in range(5):
        proposal_tmp = proposal_factory(module=module)
        token_vote_factory(token=token, content_object=proposal_tmp)

    url = reverse(
        "tokenvotes-list",
        kwargs={"module_pk": module.pk, "content_type": proposal_ct.id},
    )
    data = {"object_id": proposal.pk}
    add_token_to_session(apiclient.session, token)

    assert TokenVote.objects.all().count() == 5

    with freeze_phase(phase):
        assert apiclient.login(username=admin.email, password="password")
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert TokenVote.objects.all().count() == 5


@pytest.mark.django_db
def test_token_kept_in_session_on_login(
    apiclient,
    admin,
    voting_token_factory,
    phase_factory,
    proposal_factory,
):

    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    proposal_ct = ContentType.objects.get_for_model(proposal.__class__)
    other_proposal = proposal_factory(module=module)
    token = voting_token_factory(module=module)

    url = reverse(
        "tokenvotes-list",
        kwargs={"module_pk": module.pk, "content_type": proposal_ct.id},
    )
    add_token_to_session(apiclient.session, token)

    with freeze_phase(phase):
        data = {"object_id": proposal.pk}
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

        assert apiclient.login(username=admin.email, password="password")
        data = {"object_id": other_proposal.pk}
        session = apiclient.session
        assert "voting_tokens" in session
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_token_deleted_from_session_on_logout(
    apiclient,
    user,
    voting_token_factory,
    phase_factory,
    proposal_factory,
):

    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    proposal_ct = ContentType.objects.get_for_model(proposal.__class__)
    other_proposal = proposal_factory(module=module)
    token = voting_token_factory(module=module)

    url = reverse(
        "tokenvotes-list",
        kwargs={"module_pk": module.pk, "content_type": proposal_ct.id},
    )
    add_token_to_session(apiclient.session, token)

    with freeze_phase(phase):
        assert apiclient.login(username=user.email, password="password")
        data = {"object_id": proposal.pk}
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

        apiclient.logout()

        data = {"object_id": other_proposal.pk}
        session = apiclient.session
        assert "voting_tokens" not in session
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_voting_phase_active_valid_token_anonymous_can_delete_vote(
    apiclient, voting_token_factory, token_vote_factory, phase_factory, proposal_factory
):

    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    proposal_ct = ContentType.objects.get_for_model(proposal.__class__)
    token = voting_token_factory(module=module)
    token_vote_factory(token=token, content_object=proposal)
    add_token_to_session(apiclient.session, token)

    url = reverse(
        "tokenvotes-detail",
        kwargs={
            "module_pk": module.pk,
            "content_type": proposal_ct.id,
            "object_pk": proposal.pk,
        },
    )
    assert TokenVote.objects.all().count() == 1

    with freeze_phase(phase):
        response = apiclient.delete(url, format="json")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    assert TokenVote.objects.all().count() == 0


@pytest.mark.django_db
def test_voting_phase_active_valid_token_user_can_delete_vote(
    apiclient,
    user,
    voting_token_factory,
    token_vote_factory,
    phase_factory,
    proposal_factory,
):

    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    proposal_ct = ContentType.objects.get_for_model(proposal.__class__)
    token = voting_token_factory(module=module)
    token_vote_factory(token=token, content_object=proposal)
    add_token_to_session(apiclient.session, token)

    url = reverse(
        "tokenvotes-detail",
        kwargs={
            "module_pk": module.pk,
            "content_type": proposal_ct.id,
            "object_pk": proposal.pk,
        },
    )
    assert TokenVote.objects.all().count() == 1

    with freeze_phase(phase):
        assert apiclient.login(username=user.email, password="password")
        response = apiclient.delete(url, format="json")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    assert TokenVote.objects.all().count() == 0


@pytest.mark.django_db
def test_voting_phase_active_valid_token_admin_can_delete_vote(
    apiclient,
    admin,
    voting_token_factory,
    token_vote_factory,
    phase_factory,
    proposal_factory,
):

    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    proposal_ct = ContentType.objects.get_for_model(proposal.__class__)
    token = voting_token_factory(module=module)
    token_vote_factory(token=token, content_object=proposal)
    add_token_to_session(apiclient.session, token)

    url = reverse(
        "tokenvotes-detail",
        kwargs={
            "module_pk": module.pk,
            "content_type": proposal_ct.id,
            "object_pk": proposal.pk,
        },
    )
    assert TokenVote.objects.all().count() == 1

    with freeze_phase(phase):
        assert apiclient.login(username=admin.email, password="password")
        response = apiclient.delete(url, format="json")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    assert TokenVote.objects.all().count() == 0


@pytest.mark.django_db
def test_voting_phase_inactive_valid_token_anonymous_cannot_delete_vote(
    apiclient, voting_token_factory, token_vote_factory, phase_factory, proposal_factory
):

    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.CollectPhase
    )
    proposal_ct = ContentType.objects.get_for_model(proposal.__class__)
    token = voting_token_factory(module=module)
    token_vote_factory(token=token, content_object=proposal)
    add_token_to_session(apiclient.session, token)

    url = reverse(
        "tokenvotes-detail",
        kwargs={
            "module_pk": module.pk,
            "content_type": proposal_ct.id,
            "object_pk": proposal.pk,
        },
    )
    assert TokenVote.objects.all().count() == 1

    with freeze_phase(phase):
        response = apiclient.delete(url, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    assert TokenVote.objects.all().count() == 1


@pytest.mark.django_db
def test_voting_phase_inactive_valid_token_user_cannot_delete_vote(
    apiclient,
    user,
    voting_token_factory,
    token_vote_factory,
    phase_factory,
    proposal_factory,
):

    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.CollectPhase
    )
    proposal_ct = ContentType.objects.get_for_model(proposal.__class__)
    token = voting_token_factory(module=module)
    token_vote_factory(token=token, content_object=proposal)
    add_token_to_session(apiclient.session, token)

    url = reverse(
        "tokenvotes-detail",
        kwargs={
            "module_pk": module.pk,
            "content_type": proposal_ct.id,
            "object_pk": proposal.pk,
        },
    )
    assert TokenVote.objects.all().count() == 1

    with freeze_phase(phase):
        assert apiclient.login(username=user.email, password="password")
        response = apiclient.delete(url, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    assert TokenVote.objects.all().count() == 1


@pytest.mark.django_db
def test_voting_phase_inactive_valid_token_admin_can_delete_vote(
    apiclient,
    admin,
    voting_token_factory,
    token_vote_factory,
    phase_factory,
    proposal_factory,
):

    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.CollectPhase
    )
    proposal_ct = ContentType.objects.get_for_model(proposal.__class__)
    token = voting_token_factory(module=module)
    token_vote_factory(token=token, content_object=proposal)
    add_token_to_session(apiclient.session, token)

    url = reverse(
        "tokenvotes-detail",
        kwargs={
            "module_pk": module.pk,
            "content_type": proposal_ct.id,
            "object_pk": proposal.pk,
        },
    )
    assert TokenVote.objects.all().count() == 1

    with freeze_phase(phase):
        assert apiclient.login(username=admin.email, password="password")
        response = apiclient.delete(url, format="json")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    assert TokenVote.objects.all().count() == 0


@pytest.mark.django_db
def test_voting_phase_active_valid_token_anonymous_cannot_delete_archived(
    apiclient, voting_token_factory, token_vote_factory, phase_factory, proposal_factory
):

    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    proposal_ct = ContentType.objects.get_for_model(proposal.__class__)

    proposal.is_archived = True
    proposal.save()

    token = voting_token_factory(module=module)
    token_vote_factory(token=token, content_object=proposal)
    add_token_to_session(apiclient.session, token)

    url = reverse(
        "tokenvotes-detail",
        kwargs={
            "module_pk": module.pk,
            "content_type": proposal_ct.id,
            "object_pk": proposal.pk,
        },
    )
    assert TokenVote.objects.all().count() == 1

    with freeze_phase(phase):
        response = apiclient.delete(url, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    assert TokenVote.objects.all().count() == 1


@pytest.mark.django_db
def test_voting_phase_active_valid_token_user_cannot_delete_archived(
    apiclient,
    user,
    voting_token_factory,
    token_vote_factory,
    phase_factory,
    proposal_factory,
):

    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    proposal_ct = ContentType.objects.get_for_model(proposal.__class__)

    proposal.is_archived = True
    proposal.save()

    token = voting_token_factory(module=module)
    token_vote_factory(token=token, content_object=proposal)
    add_token_to_session(apiclient.session, token)

    url = reverse(
        "tokenvotes-detail",
        kwargs={
            "module_pk": module.pk,
            "content_type": proposal_ct.id,
            "object_pk": proposal.pk,
        },
    )
    assert TokenVote.objects.all().count() == 1

    with freeze_phase(phase):
        assert apiclient.login(username=user.email, password="password")
        response = apiclient.delete(url, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    assert TokenVote.objects.all().count() == 1


@pytest.mark.django_db
def test_voting_phase_active_valid_token_admin_can_delete_archived(
    apiclient,
    admin,
    voting_token_factory,
    token_vote_factory,
    phase_factory,
    proposal_factory,
):

    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    proposal_ct = ContentType.objects.get_for_model(proposal.__class__)

    proposal.is_archived = True
    proposal.save()

    token = voting_token_factory(module=module)
    token_vote_factory(token=token, content_object=proposal)
    add_token_to_session(apiclient.session, token)

    url = reverse(
        "tokenvotes-detail",
        kwargs={
            "module_pk": module.pk,
            "content_type": proposal_ct.id,
            "object_pk": proposal.pk,
        },
    )
    assert TokenVote.objects.all().count() == 1

    with freeze_phase(phase):
        assert apiclient.login(username=admin.email, password="password")
        response = apiclient.delete(url, format="json")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    assert TokenVote.objects.all().count() == 0


@pytest.mark.django_db
def test_voting_phase_active_no_token_cannot_delete(
    apiclient,
    admin,
    voting_token_factory,
    token_vote_factory,
    phase_factory,
    proposal_factory,
):

    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    proposal_ct = ContentType.objects.get_for_model(proposal.__class__)

    token = voting_token_factory(module=module)
    token_vote_factory(token=token, content_object=proposal)

    url = reverse(
        "tokenvotes-detail",
        kwargs={
            "module_pk": module.pk,
            "content_type": proposal_ct.id,
            "object_pk": proposal.pk,
        },
    )
    assert TokenVote.objects.all().count() == 1

    with freeze_phase(phase):
        with translation.override("en_GB"):
            assert apiclient.login(username=admin.email, password="password")
            response = apiclient.delete(url, format="json")
            assert response.status_code == status.HTTP_403_FORBIDDEN
            assert (
                "No token given or token not valid for module."
                in response.content.decode()
            )

    assert TokenVote.objects.all().count() == 1


@pytest.mark.django_db
def test_voting_phase_active_token_wrong_vote_cannot_delete(
    apiclient,
    admin,
    voting_token_factory,
    token_vote_factory,
    phase_factory,
    proposal_factory,
):

    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    proposal_ct = ContentType.objects.get_for_model(proposal.__class__)

    token = voting_token_factory(module=module)
    token_vote_factory(token=token, content_object=proposal)
    other_token = voting_token_factory(module=module)
    add_token_to_session(apiclient.session, other_token)

    url = reverse(
        "tokenvotes-detail",
        kwargs={
            "module_pk": module.pk,
            "content_type": proposal_ct.id,
            "object_pk": proposal.pk,
        },
    )
    assert TokenVote.objects.all().count() == 1

    with freeze_phase(phase):
        assert apiclient.login(username=admin.email, password="password")
        response = apiclient.delete(url, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    assert TokenVote.objects.all().count() == 1


@pytest.mark.django_db
def test_voting_phase_active_token_inactive_cannot_delete(
    apiclient,
    admin,
    voting_token_factory,
    token_vote_factory,
    phase_factory,
    proposal_factory,
):

    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    proposal_ct = ContentType.objects.get_for_model(proposal.__class__)

    token = voting_token_factory(module=module)
    token_vote_factory(token=token, content_object=proposal)
    add_token_to_session(apiclient.session, token)

    token.is_active = False
    token.save()

    url = reverse(
        "tokenvotes-detail",
        kwargs={
            "module_pk": module.pk,
            "content_type": proposal_ct.id,
            "object_pk": proposal.pk,
        },
    )
    assert TokenVote.objects.all().count() == 1

    with freeze_phase(phase):
        with translation.override("en_GB"):
            assert apiclient.login(username=admin.email, password="password")
            response = apiclient.delete(url, format="json")
            assert response.status_code == status.HTTP_403_FORBIDDEN
            assert "Token is inactive." in response.content.decode()

    assert TokenVote.objects.all().count() == 1


@pytest.mark.django_db
def test_voting_phase_active_two_valid_tokens_anonymous_can_vote_both(
    apiclient, voting_token_factory, phase_factory, proposal_factory
):

    phase_1, module_1, project_1, proposal_1 = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    phase_2, module_2, project_2, proposal_2 = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    proposal_ct = ContentType.objects.get_for_model(proposal_1.__class__)
    token_1 = voting_token_factory(module=module_1)
    token_2 = voting_token_factory(module=module_2)

    add_token_to_session(apiclient.session, token_1)

    url_1 = reverse(
        "tokenvotes-list",
        kwargs={"module_pk": module_1.pk, "content_type": proposal_ct.id},
    )

    data_1 = {"object_id": proposal_1.pk}

    with freeze_phase(phase_1):
        response = apiclient.post(url_1, data_1, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert TokenVote.objects.all().count() == 1

    url_2 = reverse(
        "tokenvotes-list",
        kwargs={"module_pk": module_2.pk, "content_type": proposal_ct.id},
    )

    data_2 = {"object_id": proposal_2.pk}

    with freeze_phase(phase_2):
        response = apiclient.post(url_2, data_2, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert TokenVote.objects.all().count() == 1

    add_token_to_session(apiclient.session, token_2)

    with freeze_phase(phase_2):
        response = apiclient.post(url_2, data_2, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert TokenVote.objects.all().count() == 2

    proposal_3 = proposal_factory(module=module_1)
    data_3 = {"object_id": proposal_3.pk}

    with freeze_phase(phase_1):
        response = apiclient.post(url_1, data_3, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert TokenVote.objects.all().count() == 3
