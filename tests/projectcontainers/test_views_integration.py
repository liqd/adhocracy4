import pytest

from adhocracy4.test.helpers import assert_template_response


@pytest.mark.django_db
def test_detail_view(client, project_container):
    url = project_container.get_absolute_url()
    response = client.get(url)
    assert_template_response(
        response, "meinberlin_projects/project_container_detail.html"
    )

    assert "meinberlin_projectcontainers/includes/container_detail.html" in (
        template.name for template in response.templates
    )
