import pytest
from django.urls import reverse

from adhocracy4.test.helpers import redirect_target


@pytest.mark.django_db
def test_module_publish_perms(client, phase, user, user2):
    module = phase.module

    module_publish_url = reverse(
        "a4dashboard:module-publish", kwargs={"module_slug": module.slug}
    )

    data = {"action": "publish"}

    response = client.post(module_publish_url, data)
    assert redirect_target(response) == "account_login"

    client.login(username=user, password="password")
    response = client.post(module_publish_url, data)
    assert response.status_code == 403

    organisation = module.project.organisation
    organisation.initiators.add(user2)
    client.login(username=user2, password="password")
    response = client.post(module_publish_url, data)
    assert redirect_target(response) == "project-edit"


@pytest.mark.django_db
def test_module_publish(client, phase, user2):
    module = phase.module
    module.is_draft = True
    module.description = ""
    module.save()
    organisation = module.project.organisation
    organisation.initiators.add(user2)

    module_publish_url = reverse(
        "a4dashboard:module-publish", kwargs={"module_slug": module.slug}
    )

    data = {"action": "publish"}

    # publishing incomplete modules has no effect
    client.login(username=user2, password="password")
    response = client.post(module_publish_url, data)
    assert redirect_target(response) == "project-edit"

    module.refresh_from_db()
    assert module.is_draft is True

    # complete module and publish it
    module.description = "module description"
    module.save()

    client.login(username=user2, password="password")
    response = client.post(module_publish_url, data)
    assert redirect_target(response) == "project-edit"

    module.refresh_from_db()
    assert module.is_draft is False


@pytest.mark.django_db
def test_module_unpublish(client, module_factory, user2):
    module = module_factory()
    module.is_draft = False
    module.save()
    project = module.project
    project.is_draft = False
    project.save()
    organisation = project.organisation
    organisation.initiators.add(user2)

    module_publish_url = reverse(
        "a4dashboard:module-publish", kwargs={"module_slug": module.slug}
    )

    data = {"action": "unpublish"}

    # unpublishing modules from published projects has no effect
    client.login(username=user2, password="password")
    response = client.post(module_publish_url, data)
    assert redirect_target(response) == "project-edit"

    module.refresh_from_db()
    assert module.is_draft is False

    # unpublish project
    project.is_draft = True
    project.save()

    # unpublishing modules that are the single module to that project
    # has no effect
    client.login(username=user2, password="password")
    response = client.post(module_publish_url, data)
    assert redirect_target(response) == "project-edit"

    module.refresh_from_db()
    assert module.is_draft is False

    # add another published module
    module_factory(project=project, is_draft=False)

    client.login(username=user2, password="password")
    response = client.post(module_publish_url, data)
    assert redirect_target(response) == "project-edit"

    module.refresh_from_db()
    assert module.is_draft is True

    # unpublishing draft modules has no effect
    client.login(username=user2, password="password")
    response = client.post(module_publish_url, data)
    assert redirect_target(response) == "project-edit"

    module.refresh_from_db()
    assert module.is_draft is True


@pytest.mark.django_db
def test_module_publish_redirect(client, module, user2):
    module_publish_url = reverse(
        "a4dashboard:module-publish", kwargs={"module_slug": module.slug}
    )

    organisation = module.project.organisation
    organisation.initiators.add(user2)

    client.login(username=user2, password="password")

    response = client.post(module_publish_url, {"referrer": "refurl"})
    assert response.status_code == 302
    assert response["location"] == "refurl"

    response = client.post(module_publish_url, {}, HTTP_REFERER="refurl")
    assert response.status_code == 302
    assert response["location"] == "refurl"

    response = client.post(module_publish_url, {})
    assert redirect_target(response) == "project-edit"
