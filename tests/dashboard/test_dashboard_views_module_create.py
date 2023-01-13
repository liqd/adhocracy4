import pytest
from django.urls import reverse
from rest_framework import status

from adhocracy4.modules.models import Module


@pytest.mark.django_db
def test_module_create(client, project, user):
    organisation = project.organisation
    organisation.initiators.add(user)

    module_create_url = reverse(
        "a4dashboard:module-create",
        kwargs={"project_slug": project.slug, "blueprint_slug": "idea-collection"},
    )

    client.login(username=user, password="password")
    response = client.post(module_create_url)
    assert response.status_code == status.HTTP_302_FOUND
    assert Module.objects.all().count() == 1
    module = Module.objects.first()
    assert response.url == reverse(
        "a4dashboard:dashboard-module_basic-edit", kwargs={"module_slug": module.slug}
    )
    assert module.project == project
    assert module.weight == 1
    assert module.blueprint_type == "IC"

    client.post(module_create_url)
    assert Module.objects.all().count() == 2
    module = Module.objects.last()
    assert module.weight == 2
