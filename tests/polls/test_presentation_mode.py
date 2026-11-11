import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_poll_defaults_to_multistep(apiclient, admin, poll_factory):
    poll = poll_factory()
    apiclient.force_authenticate(user=admin)

    url = reverse("polls-detail", kwargs={"pk": poll.pk})
    response = apiclient.get(url, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["presentation_mode"] == "multistep"


@pytest.mark.django_db
def test_poll_presentation_mode_can_be_changed(apiclient, admin, poll_factory):
    poll = poll_factory()
    apiclient.force_authenticate(user=admin)

    url = reverse("polls-detail", kwargs={"pk": poll.pk})
    response = apiclient.patch(url, {"presentation_mode": "longform"}, format="json")

    assert response.status_code == status.HTTP_200_OK
    poll.refresh_from_db()
    assert poll.presentation_mode == "longform"
    assert response.data["presentation_mode"] == "longform"
