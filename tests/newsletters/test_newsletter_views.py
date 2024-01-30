import pytest
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse

from adhocracy4.follows import models as follow_models
from adhocracy4.images.validators import ImageAltTextValidator
from adhocracy4.test.helpers import assert_template_response
from adhocracy4.test.helpers import redirect_target
from meinberlin.apps.newsletters import models as newsletter_models

User = get_user_model()


@pytest.mark.django_db
def test_send_organisation(
    admin, client, project, user_factory, follow_factory, email_address_factory
):
    organisation = project.organisation
    user1 = user_factory(get_newsletters=True)
    user2 = user_factory(get_newsletters=True)
    user_factory()
    email_address_factory(user=user1, email=user1.email, primary=True, verified=True)
    email_address_factory(user=user2, email=user2.email, primary=True, verified=True)
    follow_models.Follow.objects.all().delete()
    follow_factory(creator=user1, project=project)
    follow_factory(creator=user2, project=project, enabled=False)

    data = {
        "sender_name": "Tester",
        "sender": "test@test.de",
        "subject": "Testsubject",
        "body": "Testbody",
        "receivers": newsletter_models.ORGANISATION,
        "organisation": organisation.pk,
        "project": "",
        "send": "Send",
    }

    url = reverse(
        "a4dashboard:newsletter-create", kwargs={"organisation_slug": organisation.slug}
    )
    client.login(username=admin.email, password="password")
    response = client.post(url, data)
    assert redirect_target(response) == "newsletter-create"
    assert newsletter_models.Newsletter.objects.count() == 1
    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == [user1.email]
    assert mail.outbox[0].subject == "Testsubject"


@pytest.mark.django_db
def test_send_organisation_initiators(
    admin, client, project, user_factory, follow_factory, email_address_factory
):
    organisation = project.organisation

    assert organisation.initiators.count() == 1
    initiator = organisation.initiators.first()

    user1 = user_factory()
    email_address_factory(user=user1, email=user1.email, primary=True, verified=True)
    email_address_factory(
        user=initiator, email=initiator.email, primary=True, verified=True
    )

    follow_models.Follow.objects.all().delete()
    follow_factory(creator=user1, project=project)

    data = {
        "sender_name": "Tester",
        "sender": "test@test.de",
        "subject": "Testsubject",
        "body": "Testbody",
        "receivers": newsletter_models.INITIATOR,
        "organisation": organisation.pk,
        "project": "",
        "send": "Send",
    }

    url = reverse(
        "a4dashboard:newsletter-create", kwargs={"organisation_slug": organisation.slug}
    )
    client.login(username=admin.email, password="password")
    User.objects.update(get_newsletters=True)
    response = client.post(url, data)
    assert redirect_target(response) == "newsletter-create"
    assert newsletter_models.Newsletter.objects.count() == 1

    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == [initiator.email]
    assert mail.outbox[0].subject == "Testsubject"


@pytest.mark.django_db
def test_send_project(
    admin, client, project, user_factory, follow_factory, email_address_factory
):
    organisation = project.organisation

    user1 = user_factory(get_newsletters=True)
    user2 = user_factory()
    email_address_factory(user=user1, email=user1.email, primary=True, verified=True)
    email_address_factory(user=user2, email=user2.email, primary=True, verified=True)

    user_factory()

    follow_models.Follow.objects.all().delete()
    follow_factory(creator=user1, project=project)
    follow_factory(creator=user2, project=project, enabled=False)

    data = {
        "sender_name": "Tester",
        "sender": "test@test.de",
        "subject": "Testsubject",
        "body": "Testbody",
        "receivers": newsletter_models.PROJECT,
        "organisation": organisation.pk,
        "project": project.pk,
        "send": "Send",
    }

    url = reverse(
        "a4dashboard:newsletter-create", kwargs={"organisation_slug": organisation.slug}
    )
    client.login(username=admin.email, password="password")
    response = client.post(url, data)
    assert redirect_target(response) == "newsletter-create"
    assert newsletter_models.Newsletter.objects.count() == 1

    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == [user1.email]
    assert mail.outbox[0].subject == "Testsubject"


@pytest.mark.django_db
def test_send_project_no_project(
    admin, client, project, user_factory, follow_factory, email_address_factory
):
    organisation = project.organisation

    user1 = user_factory(get_newsletters=True)
    user2 = user_factory()
    email_address_factory(user=user1, email=user1.email, primary=True, verified=True)
    email_address_factory(user=user2, email=user2.email, primary=True, verified=True)

    user_factory()

    follow_models.Follow.objects.all().delete()
    follow_factory(creator=user1, project=project)
    follow_factory(creator=user2, project=project, enabled=False)

    data = {
        "sender_name": "Tester",
        "sender": "test@test.de",
        "subject": "Testsubject",
        "body": "Testbody",
        "receivers": newsletter_models.PROJECT,
        "organisation": organisation.pk,
        "project": "",
        "send": "Send",
    }

    url = reverse(
        "a4dashboard:newsletter-create", kwargs={"organisation_slug": organisation.slug}
    )
    client.login(username=admin.email, password="password")
    response = client.post(url, data)
    # form submit failed, still on same form page, no redirect
    assert response.status_code == 200
    assert (
        response.template_name[0]
        == "meinberlin_newsletters/newsletter_dashboard_form.html"
    )
    assert not response.context["form"].is_valid()
    assert newsletter_models.Newsletter.objects.count() == 0


@pytest.mark.django_db
def test_send_newsletter_platform(client, project, user_factory, email_address_factory):
    organisation = project.organisation

    assert organisation.initiators.count() == 1
    assert project.moderators.count() == 1
    initiator = organisation.initiators.first()
    moderator = project.moderators.first()

    admin = user_factory(is_superuser=True)
    user1 = user_factory()
    user2 = user_factory()
    User.objects.update(get_newsletters=True)
    user3 = user_factory()
    assert User.objects.count() == 6

    email_address_factory(
        user=initiator, email=initiator.email, primary=True, verified=True
    )
    email_address_factory(
        user=moderator, email=moderator.email, primary=True, verified=True
    )
    email_address_factory(user=admin, email=admin.email, primary=True, verified=True)
    email_address_factory(user=user1, email=user1.email, primary=True, verified=True)
    email_address_factory(user=user2, email=user2.email, primary=True, verified=False)
    email_address_factory(user=user3, email=user3.email, primary=True, verified=True)

    data = {
        "sender_name": "Tester",
        "sender": "test@test.de",
        "subject": "Testsubject",
        "body": "Testbody",
        "receivers": newsletter_models.PLATFORM,
        "organisation": "",
        "project": "",
        "send": "Send",
    }

    url = reverse(
        "a4dashboard:newsletter-create", kwargs={"organisation_slug": organisation.slug}
    )
    client.login(username=admin.email, password="password")
    response = client.post(url, data)
    assert redirect_target(response) == "newsletter-create"
    assert newsletter_models.Newsletter.objects.count() == 1

    assert len(mail.outbox) == 4
    to_sent = sorted([m.to[0] for m in mail.outbox])
    to_expected = sorted(
        EmailAddress.objects.filter(verified=True)
        .filter(user__get_newsletters=True)
        .values_list("email", flat=True)
    )
    assert to_sent == to_expected


@pytest.mark.django_db
def test_skip_opt_out(
    admin, client, project, user_factory, follow_factory, email_address_factory
):
    organisation = project.organisation
    user1 = user_factory(get_newsletters=False)

    email_address_factory(user=user1, email=user1.email, primary=True, verified=True)

    follow_models.Follow.objects.all().delete()
    follow_factory(creator=user1, project=project)

    data = {
        "sender_name": "Tester",
        "sender": "test@test.de",
        "subject": "Testsubject",
        "body": "Testbody",
        "receivers": newsletter_models.ORGANISATION,
        "organisation": organisation.pk,
        "project": "",
        "send": "Send",
    }

    url = reverse(
        "a4dashboard:newsletter-create", kwargs={"organisation_slug": organisation.slug}
    )
    client.login(username=admin.email, password="password")
    response = client.post(url, data)
    assert redirect_target(response) == "newsletter-create"
    assert newsletter_models.Newsletter.objects.count() == 1

    assert len(mail.outbox) == 0


@pytest.mark.django_db
def test_distinct_receivers(
    admin, client, project_factory, user_factory, follow_factory, email_address_factory
):
    project = project_factory()
    organisation = project.organisation
    project2 = project_factory(organisation=organisation)
    user1 = user_factory(get_newsletters=True)

    email_address_factory(user=user1, email=user1.email, primary=True, verified=True)

    follow_models.Follow.objects.all().delete()
    follow_factory(creator=user1, project=project)
    follow_factory(creator=user1, project=project2)

    data = {
        "sender_name": "Tester",
        "sender": "test@test.de",
        "subject": "Testsubject",
        "body": "Testbody",
        "receivers": newsletter_models.ORGANISATION,
        "organisation": organisation.pk,
        "project": "",
        "send": "Send",
    }

    url = reverse(
        "a4dashboard:newsletter-create", kwargs={"organisation_slug": organisation.slug}
    )
    client.login(username=admin.email, password="password")
    response = client.post(url, data)
    assert redirect_target(response) == "newsletter-create"
    assert newsletter_models.Newsletter.objects.count() == 1

    assert len(mail.outbox) == 1


@pytest.mark.django_db
def test_skip_inactive(
    admin, client, project, user_factory, follow_factory, email_address_factory
):
    organisation = project.organisation
    user1 = user_factory(is_active=False)

    email_address_factory(user=user1, email=user1.email, primary=True, verified=True)

    follow_models.Follow.objects.all().delete()
    follow_factory(creator=user1, project=project)

    data = {
        "sender_name": "Tester",
        "sender": "test@test.de",
        "subject": "Testsubject",
        "body": "Testbody",
        "receivers": newsletter_models.ORGANISATION,
        "organisation": organisation.pk,
        "project": "",
        "send": "Send",
    }

    url = reverse(
        "a4dashboard:newsletter-create", kwargs={"organisation_slug": organisation.slug}
    )
    client.login(username=admin.email, password="password")
    response = client.post(url, data)
    assert redirect_target(response) == "newsletter-create"
    assert newsletter_models.Newsletter.objects.count() == 1

    assert len(mail.outbox) == 0


@pytest.mark.django_db
def test_access_dashboard_newsletter(client, project, admin, user):
    organisation = project.organisation

    assert organisation.initiators.count() == 1
    initiator = organisation.initiators.first()

    url = reverse(
        "a4dashboard:newsletter-create", kwargs={"organisation_slug": organisation.slug}
    )
    client.login(username=admin.email, password="password")
    response = client.get(url)
    assert_template_response(
        response, "meinberlin_newsletters/newsletter_dashboard_form.html"
    )

    client.login(username=initiator.email, password="password")
    response = client.get(url)
    assert_template_response(
        response, "meinberlin_newsletters/newsletter_dashboard_form.html"
    )

    client.login(username=user.email, password="password")
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_limit_initiators_organisation(client, project_factory):
    project = project_factory()

    organisation = project.organisation

    assert organisation.initiators.count() == 1
    initiator = organisation.initiators.first()

    project2 = project_factory()

    url = reverse(
        "a4dashboard:newsletter-create", kwargs={"organisation_slug": organisation.slug}
    )
    client.login(username=initiator.email, password="password")

    data = {
        "sender_name": "Tester",
        "sender": "test@test.de",
        "subject": "Testsubject",
        "body": "Testbody",
        "receivers": newsletter_models.ORGANISATION,
        "organisation": project2.organisation.pk,
        "project": "",
        "send": "Send",
    }
    response = client.post(url, data)
    assert response.status_code == 403
    assert newsletter_models.Newsletter.objects.count() == 0


@pytest.mark.django_db
def test_limit_initiators_organisation_projects(client, project_factory):
    project = project_factory()

    organisation = project.organisation

    assert organisation.initiators.count() == 1
    initiator = organisation.initiators.first()

    project2 = project_factory()

    url = reverse(
        "a4dashboard:newsletter-create", kwargs={"organisation_slug": organisation.slug}
    )
    client.login(username=initiator.email, password="password")

    data = {
        "sender_name": "Tester",
        "sender": "test@test.de",
        "subject": "Testsubject",
        "body": "Testbody",
        "receivers": newsletter_models.PROJECT,
        "organisation": project.organisation.pk,
        "project": project2.pk,
        "send": "Send",
    }
    response = client.post(url, data)
    assert not response.context["form"].is_valid()
    assert newsletter_models.Newsletter.objects.count() == 0


@pytest.mark.django_db
def test_send_organisation_missing_alt_text(admin, client, project):
    organisation = project.organisation

    data = {
        "sender_name": "Tester",
        "sender": "test@test.de",
        "subject": "Testsubject",
        "body": "Testbody <img>",
        "receivers": newsletter_models.ORGANISATION,
        "organisation": organisation.pk,
        "project": "",
        "send": "Send",
    }

    url = reverse(
        "a4dashboard:newsletter-create", kwargs={"organisation_slug": organisation.slug}
    )
    client.login(username=admin.email, password="password")
    response = client.post(url, data)
    assert newsletter_models.Newsletter.objects.count() == 0
    assert "body" in response.context_data["form"].errors
    assert (
        response.context_data["form"].errors["body"][0] == ImageAltTextValidator.message
    )


@pytest.mark.django_db
def test_send_organisation_with_alt_text(
    admin, client, project, user_factory, follow_factory, email_address_factory
):
    organisation = project.organisation
    user1 = user_factory(get_newsletters=True)
    user2 = user_factory(get_newsletters=True)
    user_factory()
    email_address_factory(user=user1, email=user1.email, primary=True, verified=True)
    email_address_factory(user=user2, email=user2.email, primary=True, verified=True)
    follow_models.Follow.objects.all().delete()
    follow_factory(creator=user1, project=project)
    follow_factory(creator=user2, project=project, enabled=False)

    data = {
        "sender_name": "Tester",
        "sender": "test@test.de",
        "subject": "Testsubject",
        "body": 'Testbody <img alt="description">',
        "receivers": newsletter_models.ORGANISATION,
        "organisation": organisation.pk,
        "project": "",
        "send": "Send",
    }

    url = reverse(
        "a4dashboard:newsletter-create", kwargs={"organisation_slug": organisation.slug}
    )
    client.login(username=admin.email, password="password")
    response = client.post(url, data)
    assert redirect_target(response) == "newsletter-create"
    assert newsletter_models.Newsletter.objects.count() == 1
    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == [user1.email]
    assert mail.outbox[0].subject == "Testsubject"
