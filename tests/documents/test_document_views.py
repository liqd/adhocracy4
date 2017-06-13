from datetime import timedelta

import pytest
from django.core.urlresolvers import reverse
from freezegun import freeze_time

from adhocracy4.test.helpers import redirect_target


@pytest.mark.django_db
def test_paragraph_detail_view(client, paragraph_factory, phase_factory):
    phase = phase_factory()
    paragraph = paragraph_factory(chapter__module=phase.module)

    url = reverse(
        'meinberlin_documents:paragraph-detail',
        kwargs={'pk': paragraph.pk}
    )

    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_paragraph_private_detail_view(client, paragraph_factory, user,
                                       phase_factory):
    phase = phase_factory(module__project__is_public=False)
    paragraph = paragraph_factory(chapter__module=phase.module)

    url = reverse(
        'meinberlin_documents:paragraph-detail',
        kwargs={'pk': paragraph.pk}
    )

    response = client.get(url)
    assert redirect_target(response) == 'account_login'

    client.login(username=user.email, password='password')
    response = client.get(url)
    assert response.status_code == 403

    paragraph.project.participants.add(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_paragraph_pre_phase_detail_view(client, paragraph_factory, user,
                                         phase_factory):
    phase = phase_factory()
    paragraph = paragraph_factory(chapter__module=phase.module)

    url = reverse(
        'meinberlin_documents:paragraph-detail',
        kwargs={'pk': paragraph.pk}
    )

    with freeze_time(phase.start_date - timedelta(days=1)):
        response = client.get(url)
        assert redirect_target(response) == 'account_login'

        client.login(username=user.email, password='password')
        response = client.get(url)
        assert response.status_code == 403


@pytest.mark.django_db
def test_chapter_pre_phase_detail_view(client, chapter_factory, user,
                                       phase_factory):
    phase = phase_factory()
    chapter = chapter_factory(module=phase.module)

    url = reverse(
        'meinberlin_documents:chapter-detail',
        kwargs={'pk': chapter.pk}
    )

    with freeze_time(phase.start_date - timedelta(days=1)):
        response = client.get(url)
        assert redirect_target(response) == 'account_login'

        client.login(username=user.email, password='password')
        response = client.get(url)
        assert response.status_code == 403
