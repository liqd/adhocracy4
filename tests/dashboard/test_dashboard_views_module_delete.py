import pytest
from django.urls import reverse

from adhocracy4.modules.models import Module
from adhocracy4.test.helpers import redirect_target


@pytest.mark.django_db
def test_module_delete_perms(client, phase, user, user2):
    module = phase.module

    module_delete_url = reverse(
        "a4dashboard:module-delete", kwargs={"slug": module.slug}
    )

    response = client.post(module_delete_url)
    assert redirect_target(response) == "account_login"

    client.login(username=user, password="password")
    response = client.post(module_delete_url)
    assert response.status_code == 403

    organisation = module.project.organisation
    organisation.initiators.add(user2)
    client.login(username=user2, password="password")
    response = client.post(module_delete_url)
    assert redirect_target(response) == "project-edit"


@pytest.mark.django_db
def test_module_delete(client, phase, user2):
    module = phase.module
    module.is_draft = False
    module.save()
    organisation = module.project.organisation
    organisation.initiators.add(user2)
    assert Module.objects.all().count() == 1

    module_delete_url = reverse(
        "a4dashboard:module-delete", kwargs={"slug": module.slug}
    )

    # deleting published modules has no effect
    client.login(username=user2, password="password")
    response = client.post(module_delete_url)
    assert response.status_code == 302
    assert Module.objects.all().count() == 1

    # unpublish module
    module.is_draft = True
    module.save()

    client.login(username=user2, password="password")
    response = client.post(module_delete_url)
    assert redirect_target(response) == "project-edit"
    assert Module.objects.all().count() == 0


@pytest.mark.django_db
def test_module_delete_redirect(client, module_factory, user2):
    module = module_factory(is_draft=True)
    organisation = module.project.organisation
    organisation.initiators.add(user2)
    module_2 = module_factory(project=module.project, is_draft=True)
    module_3 = module_factory(project=module.project, is_draft=True)

    module_delete_url = reverse(
        "a4dashboard:module-delete", kwargs={"slug": module.slug}
    )
    module_delete_url_2 = reverse(
        "a4dashboard:module-delete", kwargs={"slug": module_2.slug}
    )
    module_delete_url_3 = reverse(
        "a4dashboard:module-delete", kwargs={"slug": module_3.slug}
    )

    client.login(username=user2, password="password")

    referrer = reverse(
        "a4dashboard:dashboard-information-edit",
        kwargs={"project_slug": module.project.slug},
    )

    response = client.post(module_delete_url, {"referrer": referrer})
    assert response.status_code == 302
    assert response["location"] == referrer

    response = client.post(module_delete_url_2, {}, HTTP_REFERER=referrer)
    assert response.status_code == 302
    assert response["location"] == referrer

    response = client.post(module_delete_url_3, {})
    assert redirect_target(response) == "project-edit"


@pytest.mark.django_db
def test_module_unsuccessful_delete_redirect(client, module_factory, user2):
    module = module_factory(is_draft=False)
    organisation = module.project.organisation
    organisation.initiators.add(user2)

    module_delete_url = reverse(
        "a4dashboard:module-delete", kwargs={"slug": module.slug}
    )

    client.login(username=user2, password="password")

    referrer = reverse(
        "a4dashboard:dashboard-information-edit",
        kwargs={"project_slug": module.project.slug},
    )

    response = client.post(module_delete_url, {"referrer": referrer})
    assert response.status_code == 302
    assert response["location"] == referrer

    response = client.post(module_delete_url, {}, HTTP_REFERER=referrer)
    assert response.status_code == 302
    assert response["location"] == referrer

    response = client.post(module_delete_url, {})
    assert redirect_target(response) == "project-edit"
