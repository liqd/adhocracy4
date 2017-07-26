import pytest
from datetime import timedelta
from django.core.urlresolvers import reverse
from freezegun import freeze_time

from adhocracy4.test.helpers import redirect_target


@pytest.mark.django_db
def test_detail_view_module(client, phase):
    module = phase.module
    module_url = reverse('module-detail', args=[module.slug])
    with freeze_time(phase.start_date - timedelta(days=1)):
        response = client.get(module_url)
        assert response.status_code == 200
    with freeze_time(phase.start_date):
        response = client.get(module_url)
        assert redirect_target(response) == 'project-detail'
        assert module.project.get_absolute_url() in response.url
    with freeze_time(phase.end_date):
        response = client.get(module_url)
        assert response.status_code == 200
