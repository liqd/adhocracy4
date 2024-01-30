import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse

from adhocracy4.images.validators import ImageAltTextValidator
from adhocracy4.test.helpers import assert_template_response
from adhocracy4.test.helpers import redirect_target
from meinberlin.apps.platformemails import models as platformemail_models

User = get_user_model()


@pytest.mark.django_db
def test_send_platform_email(client, user_factory, email_address_factory):
    admin = user_factory(is_superuser=True)
    user1 = user_factory(get_newsletters=True)
    user2 = user_factory(get_newsletters=True)
    user3 = user_factory()
    assert User.objects.count() == 4

    email_address_factory(user=admin, email=admin.email, primary=True, verified=True)
    email_address_factory(user=user1, email=user1.email, primary=True, verified=True)
    email_address_factory(user=user2, email=user2.email, primary=True, verified=False)
    email_address_factory(user=user3, email=user3.email, primary=True, verified=True)

    data = {
        "sender_name": "Tester",
        "sender": "test@test.de",
        "subject": "Testsubject",
        "body": "Testbody",
        "send": "Send",
    }

    url = reverse("meinberlin_platformemails:create")
    client.login(username=admin.email, password="password")
    response = client.post(url, data)
    assert redirect_target(response) == "create"
    assert platformemail_models.PlatformEmail.objects.count() == 1

    assert len(mail.outbox) == 3
    to_sent = sorted([m.to[0] for m in mail.outbox])
    to_expected = sorted([admin.email, user1.email, user3.email])
    assert to_sent == to_expected


@pytest.mark.django_db
def test_access_admin_platform_email(client, project, admin, user_factory):
    organisation = project.organisation

    assert organisation.initiators.count() == 1
    initiator = organisation.initiators.first()

    user = user_factory()

    url = reverse("meinberlin_platformemails:create")

    client.login(username=admin.email, password="password")
    response = client.get(url)
    assert_template_response(
        response, "meinberlin_platformemails/platformemail_form.html"
    )

    client.login(username=initiator.email, password="password")
    response = client.get(url)
    assert response.status_code == 403

    client.login(username=user.email, password=user.password)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_send_platform_email_missing_alt_text(
    client, user_factory, email_address_factory
):
    admin = user_factory(is_superuser=True)
    email_address_factory(user=admin, email=admin.email, primary=True, verified=True)

    data = {
        "sender_name": "Tester",
        "sender": "test@test.de",
        "subject": "Testsubject",
        "body": "Testbody <img>",
        "send": "Send",
    }

    url = reverse("meinberlin_platformemails:create")
    client.login(username=admin.email, password="password")
    response = client.post(url, data)
    assert platformemail_models.PlatformEmail.objects.count() == 0
    assert "body" in response.context_data["form"].errors
    assert (
        response.context_data["form"].errors["body"][0] == ImageAltTextValidator.message
    )


@pytest.mark.django_db
def test_send_platform_email_has_alt_text(client, user_factory, email_address_factory):
    admin = user_factory(is_superuser=True)
    user1 = user_factory(get_newsletters=True)
    user2 = user_factory(get_newsletters=True)
    user3 = user_factory()
    assert User.objects.count() == 4

    email_address_factory(user=admin, email=admin.email, primary=True, verified=True)
    email_address_factory(user=user1, email=user1.email, primary=True, verified=True)
    email_address_factory(user=user2, email=user2.email, primary=True, verified=False)
    email_address_factory(user=user3, email=user3.email, primary=True, verified=True)

    data = {
        "sender_name": "Tester",
        "sender": "test@test.de",
        "subject": "Testsubject",
        "body": 'Testbody <img alt="description">',
        "send": "Send",
    }

    url = reverse("meinberlin_platformemails:create")
    client.login(username=admin.email, password="password")
    response = client.post(url, data)
    assert redirect_target(response) == "create"
    assert platformemail_models.PlatformEmail.objects.count() == 1

    assert len(mail.outbox) == 3
    to_sent = sorted([m.to[0] for m in mail.outbox])
    to_expected = sorted([admin.email, user1.email, user3.email])
    assert to_sent == to_expected
