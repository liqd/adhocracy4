import pytest

from adhocracy4.test.helpers import assert_template_response


@pytest.mark.django_db
def test_detail_view(client, offline_event):
    url = offline_event.get_absolute_url()
    response = client.get(url)
    assert_template_response(
        response, 'meinberlin_projects/project_detail.html')
