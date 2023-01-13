import pytest
from django.urls import reverse

from adhocracy4.test.helpers import assert_template_response


@pytest.mark.django_db
def test_chapter_detail_view_redirect_first_chapter(
    client, chapter_factory, phase_factory
):
    phase = phase_factory()
    chapter = chapter_factory(module=phase.module)

    url = reverse("meinberlin_documents:chapter-detail", kwargs={"pk": chapter.pk})

    response = client.get(url)
    assert_template_response(response, "meinberlin_documents/chapter_detail.html")
