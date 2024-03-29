import pytest

from adhocracy4.dashboard import components
from adhocracy4.test.helpers import assert_template_response
from adhocracy4.test.helpers import redirect_target

component = components.projects.get("result")


@pytest.mark.django_db
def test_edit_view(client, project, admin):
    url = component.get_base_url(project)
    client.login(username=admin.username, password="password")
    response = client.get(url)
    assert_template_response(response, "a4dashboard/base_form_project.html")

    data = {
        "result": "<p>some long result text</p>",
    }
    response = client.post(url, data)
    assert redirect_target(response) == "dashboard-result-edit"
    project.refresh_from_db()
    assert project.result == data.get("result")
