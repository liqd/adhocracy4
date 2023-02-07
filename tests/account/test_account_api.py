import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_end_session(
    apiclient,
    client,
    user,
):
    apiclient.login(username=user.email, password="password")
    session_key = apiclient.session.session_key
    assert apiclient.session.exists(session_key)
    assert apiclient.cookies["sessionid"].value
    url_profile = reverse("account_profile")
    response = apiclient.get(url_profile)
    assert response.status_code == status.HTTP_200_OK

    url_end_session = reverse("end_session")
    response = apiclient.get(url_end_session)
    assert response.status_code == status.HTTP_200_OK

    # check that session is empty and session cookie deleted
    assert apiclient.session.is_empty()
    assert not apiclient.cookies["sessionid"].value
    response = apiclient.get(url_profile)
    assert response.status_code == status.HTTP_302_FOUND
    assert response.url.startswith(reverse("account_login"))
