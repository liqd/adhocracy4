import pytest

from adhocracy4.dashboard import components
from adhocracy4.test.helpers import redirect_target

component = components.projects.get('information')


@pytest.mark.django_db
def test_edit_view(client, project, admin):
    url = component.get_base_url(project)
    client.login(username=admin.username, password='password')
    response = client.get(url)
    assert response.status_code == 200

    data = {
        'information': '<p>some information text</p>',
        'contact_name': 'contact name',
        'contact_address_text': 'some street 43',
        'contact_phone': '+49 30 1234 5678',
        'contact_email': 'someone@example.com',
        'contact_url': 'https://example.com',
    }
    response = client.post(url, data)
    assert redirect_target(response) == 'dashboard-information-edit'
    project.refresh_from_db()
    assert project.information == data.get('information')
    assert project.contact_name == data.get('contact_name')
    assert project.contact_address_text == \
        data.get('contact_address_text')
    assert project.contact_phone == data.get('contact_phone')
    assert project.contact_email == data.get('contact_email')
    assert project.contact_url == data.get('contact_url')
