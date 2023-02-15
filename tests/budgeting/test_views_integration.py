import pytest
from dateutil.parser import parse
from django.core import mail
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from adhocracy4.test.helpers import assert_template_response
from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import freeze_post_phase
from adhocracy4.test.helpers import freeze_time
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
def test_list_view_qs_gets_annotated(client, phase_factory, proposal_factory):
    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    url = project.get_absolute_url()

    with freeze_phase(phase):
        response = client.get(url)
        annotated_proposal = response.context_data["proposal_list"][0]
        assert hasattr(annotated_proposal, "comment_count")
        assert hasattr(annotated_proposal, "positive_rating_count")
        assert hasattr(annotated_proposal, "negative_rating_count")
        assert hasattr(annotated_proposal, "token_vote_count")


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
def test_list_view_default_filters(client, module, phase_factory, proposal_factory):
    support_phase = phase_factory(
        phase_content=phases.SupportPhase(),
        module=module,
        start_date=parse("2022-01-01 00:00:00 UTC"),
        end_date=parse("2022-01-01 10:00:00 UTC"),
    )
    voting_phase = phase_factory(
        phase_content=phases.VotingPhase(),
        module=module,
        start_date=parse("2022-01-01 14:00:00 UTC"),
        end_date=parse("2022-01-01 18:00:00 UTC"),
    )

    between_phases = parse("2022-01-01 12:00:00 UTC")

    url = module.get_absolute_url()
    with freeze_phase(support_phase):
        response = client.get(url)
        defaults = response.context["view"].filter_set.defaults
        assert "is_archived" in defaults
        assert defaults["is_archived"] == "false"
        assert "ordering" in defaults
        assert defaults["ordering"] == "dailyrandom"

    with freeze_time(between_phases):
        response = client.get(url)
        defaults = response.context["view"].filter_set.defaults
        assert "is_archived" in defaults
        assert defaults["is_archived"] == "false"
        assert "ordering" in defaults
        assert defaults["ordering"] == "-positive_rating_count"

    with freeze_phase(voting_phase):
        response = client.get(url)
        defaults = response.context["view"].filter_set.defaults
        assert "is_archived" in defaults
        assert defaults["is_archived"] == "false"
        assert "ordering" in defaults
        assert defaults["ordering"] == "dailyrandom"

    with freeze_post_phase(voting_phase):
        response = client.get(url)
        defaults = response.context["view"].filter_set.defaults
        assert "is_archived" in defaults
        assert defaults["is_archived"] == "false"
        assert "ordering" in defaults
        assert defaults["ordering"] == "-token_vote_count"


@pytest.mark.django_db
def test_list_view_token_form(
    client, user, phase_factory, proposal_factory, voting_token_factory, module_factory
):
    phase, module, project, item = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    url = project.get_absolute_url()
    token = voting_token_factory(module=module)

    data = {"token": str(token)}

    with freeze_phase(phase):
        response = client.get(url)
        assert "token_form" in response.context
        assert_template_response(response, "meinberlin_budgeting/proposal_list.html")
        assert not response.context["valid_token_present"]

        response = client.post(url, data)
        assert response.status_code == 200
        assert "voting_tokens" in client.session
        assert "token_expire_date" in client.session
        assert "token_form" in response.context

        response = client.get(url)
        assert response.context["valid_token_present"]

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
def test_list_view_tokens_for_different_modules(
    client, phase_factory, proposal_factory, voting_token_factory
):
    phase_1, module_1, _, _ = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    url_1 = module_1.get_absolute_url()
    token_1 = voting_token_factory(module=module_1)
    data_1 = {"token": str(token_1)}

    with freeze_phase(phase_1):
        response = client.post(url_1, data_1)
        assert response.status_code == 200
        assert "voting_tokens" in client.session
        assert str(module_1.id) in client.session["voting_tokens"]

        response = client.get(url_1)
        assert response.context["valid_token_present"]

    phase_2, module_2, _, _ = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    url_2 = module_2.get_absolute_url()
    token_2 = voting_token_factory(module=module_2)
    data_2 = {"token": str(token_2)}

    with freeze_phase(phase_2):
        response = client.post(url_2, data_2)
        assert response.status_code == 200
        assert "voting_tokens" in client.session
        assert str(module_2.id) in client.session["voting_tokens"]
        assert str(module_1.id) in client.session["voting_tokens"]

        response = client.get(url_2)
        assert response.context["valid_token_present"]

        response = client.get(url_1)
        assert response.context["valid_token_present"]


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
    filter_string = "?mode=list&is_archived=&page=1&search="
    filtered_project_referer = project_referer + filter_string
    filtered_module_referer = module_referer + filter_string
    with freeze_phase(phase):
        response = client.get(url, HTTP_referer=project_referer)
        assert response.context["back"] == "{}#proposal_{}".format(
            project_referer, item.id
        )
        assert response.context["back_string"] == _("map")
        response = client.get(url, HTTP_referer=module_referer)
        assert response.context["back"] == "{}#proposal_{}".format(
            module_referer, item.id
        )
        assert response.context["back_string"] == _("map")

        response = client.get(url, HTTP_referer=filtered_project_referer)
        assert response.context["back"] == "{}#proposal_{}".format(
            filtered_project_referer, item.id
        )
        assert response.context["back_string"] == _("list")
        response = client.get(url, HTTP_referer=filtered_module_referer)
        assert response.context["back"] == "{}#proposal_{}".format(
            filtered_module_referer, item.id
        )
        assert response.context["back_string"] == _("list")

        response = client.get(url, HTTP_referer="/")
        assert response.context["back"] == module.get_detail_url
        assert response.context["back_string"] == _("map")
        response = client.get(url)
        assert response.context["back"] == module.get_detail_url
        assert response.context["back_string"] == _("map")


@pytest.mark.django_db
def test_detail_view_token_in_session(
    client, phase_factory, proposal_factory, voting_token_factory
):
    phase_1, module_1, project_1, proposal_1 = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )

    phase_2, module_2, project_2, proposal_2 = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )

    token_1 = voting_token_factory(module=module_1)
    project_url = project_1.get_absolute_url()
    data = {"token": str(token_1)}

    proposal_1_url = proposal_1.get_absolute_url()
    proposal_2_url = proposal_2.get_absolute_url()

    with freeze_phase(phase_1):
        response = client.get(proposal_1_url)
        assert not response.context_data["has_valid_token_in_session"]

        client.post(project_url, data)

        response = client.get(proposal_1_url)
        assert response.context_data["has_valid_token_in_session"]

    with freeze_phase(phase_2):
        response = client.get(proposal_2_url)
        assert not response.context_data["has_valid_token_in_session"]


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
