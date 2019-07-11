import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_chapter_detail_view_redirect_first_chapter(client, chapter_factory,
                                                    phase_factory):
    phase = phase_factory()
    chapter = chapter_factory(module=phase.module)

    url = reverse(
        'meinberlin_documents:chapter-detail',
        kwargs={'pk': chapter.pk}
    )

    response = client.get(url)
    assert response.status_code == 200
