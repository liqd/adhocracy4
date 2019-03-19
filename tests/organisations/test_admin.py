import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_organisation_admin_form(client, organisation,
                                 admin, user_factory,
                                 group_factory):

    client.login(username=admin, password='password')
    url = reverse('admin:meinberlin_organisations_organisation_add')
    response = client.get(url)
    assert response.status_code == 200

    data = {'name': 'My Organisation'}
    response = client.post(url, data)

    assert 1 == 2
