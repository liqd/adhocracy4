import pytest
from django.core.urlresolvers import reverse


@pytest.mark.django_db
def test_detail_view(client, module):
    module_url = reverse('module-detail', args=[module.slug])
    response = client.get(module_url)
    assert response.status_code == 200
