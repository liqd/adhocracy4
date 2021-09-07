import pytest
from django.urls import reverse

from adhocracy4.test.helpers import redirect_target


@pytest.mark.django_db
def test_module_delete_perms(client, phase, user, user2):
    module = phase.module

    module_delete_url = reverse('a4dashboard:module-delete', kwargs={
        'slug': module.slug})

    response = client.post(module_delete_url)
    assert redirect_target(response) == 'account_login'

    client.login(username=user, password='password')
    response = client.post(module_delete_url)
    assert response.status_code == 403

    organisation = module.project.organisation
    organisation.initiators.add(user2)
    client.login(username=user2, password='password')
    response = client.post(module_delete_url)
    assert redirect_target(response) == 'project-edit'
