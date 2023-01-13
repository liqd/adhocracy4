import pytest
from django.urls import reverse

from meinberlin.apps.budgeting.models import Proposal


@pytest.mark.django_db
def test_proposal_list_pagination(apiclient, module, proposal_factory):

    url = reverse("proposals-list", kwargs={"module_pk": module.pk})
    response = apiclient.get(url)
    pagesize = response.data["page_size"]
    num_props = pagesize * 3 + 1

    for i in range(num_props):
        proposal_factory(module=module)

    response = apiclient.get(url)

    assert "count" in response.data
    assert "page_count" in response.data
    assert response.data["count"] == num_props
    assert response.data["next"].endswith("?page=2")
    assert not response.data["previous"]
    assert response.data["page_count"] == 4
    assert len(response.data["results"]) == pagesize

    url_tmp = url + "?page=4"
    response = apiclient.get(url_tmp)
    assert not response.data["next"]
    assert response.data["previous"].endswith("?page=3")
    assert len(response.data["results"]) == 1

    proposal = Proposal.objects.last()
    proposal.is_archived = True
    proposal.save()

    url_tmp = url + "?is_archived=false"
    response = apiclient.get(url_tmp)
    assert response.data["next"]
    assert not response.data["previous"]
    assert response.data["page_count"] == 3
    assert len(response.data["results"]) == pagesize
