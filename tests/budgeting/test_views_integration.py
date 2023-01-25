import pytest
from django.core import mail
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from adhocracy4.test.helpers import assert_template_response
from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import redirect_target
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.budgeting import models
from meinberlin.apps.budgeting import phases
from meinberlin.apps.budgeting import views


@pytest.mark.django_db
def test_list_view(client, phase_factory, proposal_factory):
    phase, module, project, item = setup_phase(
        phase_factory, proposal_factory, phases.RequestPhase
    )
    url = project.get_absolute_url()
    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(response, "meinberlin_budgeting/proposal_list.html")


@pytest.mark.django_db
def test_list_view_ordering_choices(client, phase_factory, proposal_factory):
    phase, module, project, item = setup_phase(
        phase_factory, proposal_factory, phases.RatingPhase
    )
    url = project.get_absolute_url()
    with freeze_phase(phase):
        response = client.get(url)
        view = response.context["view"]
        ordering_choices = views.get_ordering_choices(view)
        assert ordering_choices == (
            ("-created", _("Most recent")),
            ("-positive_rating_count", _("Most popular")),
            ("-comment_count", _("Most commented")),
            ("dailyrandom", _("Random")),
        )

    phase, module, project, item = setup_phase(
        phase_factory, proposal_factory, phases.SupportPhase
    )
    url = project.get_absolute_url()
    with freeze_phase(phase):
        response = client.get(url)
        view = response.context["view"]
        ordering_choices = views.get_ordering_choices(view)
        assert ordering_choices == (
            ("-created", _("Most recent")),
            ("-positive_rating_count", _("Most support")),
            ("-comment_count", _("Most commented")),
            ("dailyrandom", _("Random")),
        )


@pytest.mark.django_db
def test_list_view_token_form(
    client, user, phase_factory, proposal_factory, voting_token_factory, module_factory
):
    phase, module, project, item = setup_phase(
        phase_factory, proposal_factory, phases.RequestPhase
    )
    url = project.get_absolute_url()
    token = voting_token_factory(module=module)

    data = {"token": str(token)}

    with freeze_phase(phase):
        response = client.get(url)
        assert "token_form" in response.context
        assert_template_response(response, "meinberlin_budgeting/proposal_list.html")

        response = client.post(url, data)
        assert response.status_code == 200
        assert "voting_tokens" in client.session
        assert "token_form" in response.context

    other_module = module_factory()
    other_token = voting_token_factory(module=other_module)

    # remove token from session
    client.login(username=user.email, password="password")
    client.logout()

    data = {"token": str(other_token)}

    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(response, "meinberlin_budgeting/proposal_list.html")

        response = client.post(url, data)
        assert "token" in response.context_data["token_form"].errors
        msg = _("This token is not valid")
        assert msg in response.context_data["token_form"].errors["token"]
        assert "voting_tokens" not in client.session


@pytest.mark.django_db
def test_detail_view(client, phase_factory, proposal_factory):
    phase, module, project, item = setup_phase(
        phase_factory, proposal_factory, phases.RequestPhase
    )
    url = item.get_absolute_url()
    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(response, "meinberlin_budgeting/proposal_detail.html")


@pytest.mark.django_db
def test_detail_view_back_link(client, phase_factory, proposal_factory):
    phase, module, project, item = setup_phase(
        phase_factory, proposal_factory, phases.RequestPhase
    )
    url = item.get_absolute_url()
    project_referer = reverse("project-detail", kwargs={"slug": item.project.slug})
    module_referer = reverse("module-detail", kwargs={"module_slug": item.module.slug})
    filter_string = "?is_archived=&page=1&search="
    filtered_project_referer = project_referer + filter_string
    filtered_module_referer = module_referer + filter_string
    with freeze_phase(phase):
        response = client.get(url, HTTP_referer=project_referer)
        assert response.context["back"] == "{}#proposal_{}".format(
            project_referer, item.id
        )
        response = client.get(url, HTTP_referer=module_referer)
        assert response.context["back"] == "{}#proposal_{}".format(
            module_referer, item.id
        )

        response = client.get(url, HTTP_referer=filtered_project_referer)
        assert response.context["back"] == "{}#proposal_{}".format(
            filtered_project_referer, item.id
        )
        response = client.get(url, HTTP_referer=filtered_module_referer)
        assert response.context["back"] == "{}#proposal_{}".format(
            filtered_module_referer, item.id
        )

        response = client.get(url, HTTP_referer="/")
        assert not response.context["back"]
        response = client.get(url)
        assert not response.context["back"]


@pytest.mark.django_db
def test_create_view(
    client,
    phase_factory,
    proposal_factory,
    user,
    category_factory,
    area_settings_factory,
):
    phase, module, project, item = setup_phase(
        phase_factory, proposal_factory, phases.RequestPhase
    )
    area_settings_factory(module=module)
    category = category_factory(module=module)
    url = reverse(
        "meinberlin_budgeting:proposal-create", kwargs={"module_slug": module.slug}
    )
    with freeze_phase(phase):
        client.login(username=user.email, password="password")

        response = client.get(url)
        assert_template_response(
            response, "meinberlin_budgeting/proposal_create_form.html"
        )

        data = {
            "name": "Idea",
            "description": "description",
            "category": category.pk,
            "budget": 123,
            "point": (0, 0),
            "point_label": "somewhere",
            "allow_contact": False,
        }
        response = client.post(url, data)
        assert redirect_target(response) == "proposal-detail"


@pytest.mark.django_db
def test_update_view(
    client,
    phase_factory,
    proposal_factory,
    user,
    category_factory,
    area_settings_factory,
):
    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.RequestPhase
    )
    area_settings_factory(module=module)
    category = category_factory(module=module)
    url = reverse(
        "meinberlin_budgeting:proposal-update",
        kwargs={"pk": "{:05d}".format(proposal.pk), "year": proposal.created.year},
    )
    with freeze_phase(phase):
        client.login(username=user.email, password="password")
        response = client.get(url)
        assert response.status_code == 403

        client.login(username=proposal.creator.email, password="password")
        response = client.get(url)
        assert_template_response(
            response, "meinberlin_budgeting/proposal_update_form.html"
        )

        data = {
            "name": "Idea",
            "description": "super new description",
            "category": category.pk,
            "budget": 123,
            "point": (0, 0),
            "point_label": "somewhere",
            "allow_contact": False,
        }
        response = client.post(url, data)
        assert response.status_code == 302
        assert redirect_target(response) == "proposal-detail"
        updated_proposal = models.Proposal.objects.get(id=proposal.pk)
        assert updated_proposal.description == "super new description"


@pytest.mark.django_db
def test_moderate_view(
    client, phase_factory, proposal_factory, user, area_settings_factory
):
    phase, module, project, item = setup_phase(
        phase_factory, proposal_factory, phases.RequestPhase
    )
    item.contact_email = "user_test@liqd.net"
    item.save()
    area_settings_factory(module=module)
    url = reverse(
        "meinberlin_budgeting:proposal-moderate",
        kwargs={"pk": item.pk, "year": item.created.year},
    )
    project.moderators.set([user])
    with freeze_phase(phase):
        client.login(username=user.email, password="password")

        response = client.get(url)
        assert_template_response(
            response, "meinberlin_budgeting/proposal_moderate_form.html"
        )

        data = {
            "moderator_status": "test",
            "is_archived": False,
            "statement": "its a statement",
            "remark": "this is a remark",
        }
        response = client.post(url, data)
        assert redirect_target(response) == "proposal-detail"

        # was the NotifyCreatorOrContactOnModeratorFeedback sent?
        assert len(mail.outbox) == 1
        assert mail.outbox[0].to == [item.contact_email]
        assert mail.outbox[0].subject.startswith("Rückmeldung")


@pytest.mark.django_db
def test_moderate_view_with_tasks(
    client,
    phase_factory,
    proposal_factory,
    user,
    area_settings_factory,
    moderation_task_factory,
):
    phase, module, project, item = setup_phase(
        phase_factory, proposal_factory, phases.RequestPhase
    )
    item.contact_email = "user_test@liqd.net"
    item.save()
    area_settings_factory(module=module)
    url = reverse(
        "meinberlin_budgeting:proposal-moderate",
        kwargs={"pk": item.pk, "year": item.created.year},
    )
    project.moderators.set([user])
    task1 = moderation_task_factory(module=module)
    task2 = moderation_task_factory(module=module)
    with freeze_phase(phase):
        client.login(username=user.email, password="password")

        response = client.get(url)
        assert_template_response(
            response, "meinberlin_budgeting/proposal_moderate_form.html"
        )

        data = {
            "moderator_status": "test",
            "is_archived": False,
            "feedback_text": "its a moderator feedback text",
            "remark": "this is a remark",
            "completed_tasks": [task1.pk, task2.pk],
        }
        response = client.post(url, data)
        assert redirect_target(response) == "proposal-detail"

        # was the NotifyCreatorOrContactOnModeratorFeedback sent?
        assert len(mail.outbox) == 1
        assert mail.outbox[0].to == [item.contact_email]
        assert mail.outbox[0].subject.startswith("Rückmeldung")


@pytest.mark.django_db
def test_moderate_view_same_creator_contact(
    client, phase_factory, proposal_factory, user, area_settings_factory
):
    phase, module, project, item = setup_phase(
        phase_factory, proposal_factory, phases.RequestPhase
    )
    item.contact_email = item.creator.email
    item.save()
    area_settings_factory(module=module)
    url = reverse(
        "meinberlin_budgeting:proposal-moderate",
        kwargs={"pk": item.pk, "year": item.created.year},
    )
    project.moderators.set([user])
    with freeze_phase(phase):
        client.login(username=user.email, password="password")

        response = client.get(url)
        assert_template_response(
            response, "meinberlin_budgeting/proposal_moderate_form.html"
        )

        data = {
            "moderator_status": "test",
            "is_archived": False,
            "feedback_text": "its a moderator feedback text",
        }
        response = client.post(url, data)
        assert redirect_target(response) == "proposal-detail"

        # was the NotifyCreatorOrContactOnModeratorFeedback sent,
        # even though the contact email is the same as the creator's?
        assert len(mail.outbox) == 1
        assert mail.outbox[0].to == [item.contact_email]
        assert mail.outbox[0].subject.startswith("Rückmeldung")


@pytest.mark.django_db
def test_export_view(client, proposal_factory, module_factory):
    proposal = proposal_factory()
    organisation = proposal.module.project.organisation
    initiator = organisation.initiators.first()
    client.login(username=initiator.email, password="password")
    url = reverse(
        "a4dashboard:budgeting-export", kwargs={"module_slug": proposal.module.slug}
    )
    response = client.get(url)
    assert response.status_code == 200
    assert (
        response["Content-Type"] == "application/vnd.openxmlformats-officedocument."
        "spreadsheetml.sheet"
    )
