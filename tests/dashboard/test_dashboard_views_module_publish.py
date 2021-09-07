import pytest
from django.urls import reverse

from adhocracy4.test.helpers import redirect_target


@pytest.mark.django_db
def test_module_publish_perms(client, phase, user, user2):
    module = phase.module

    module_publish_url = reverse('a4dashboard:module-publish', kwargs={
        'module_slug': module.slug})

    data = {'action': 'publish'}

    response = client.post(module_publish_url, data)
    assert redirect_target(response) == 'account_login'

    client.login(username=user, password='password')
    response = client.post(module_publish_url, data)
    assert response.status_code == 403

    organisation = module.project.organisation
    organisation.initiators.add(user2)
    client.login(username=user2, password='password')
    response = client.post(module_publish_url, data)
    assert redirect_target(response) == 'project-edit'
