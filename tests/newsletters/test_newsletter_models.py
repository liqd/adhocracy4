import pytest
from django.conf import settings


@pytest.mark.django_db
def test_absolute_media_urls(newsletter_factory):
    base = (
        "Relative {rel}test.png"
        "Tag1: href={rel}test.png"
        'Tag2: href="{rel}test.png"'
        "Tag3: href='{rel}test.png'"
        "Absolute: http://foo.bar/{abs}test.png"
    )

    body = base.format(rel=settings.MEDIA_URL, abs=settings.MEDIA_URL)
    newsletter = newsletter_factory(body=body)

    expected = base.format(
        rel=settings.WAGTAILADMIN_BASE_URL + settings.MEDIA_URL, abs=settings.MEDIA_URL
    )
    assert body == newsletter.body
    assert expected == newsletter.body_with_absolute_urls


@pytest.mark.django_db
def test_invalidate_cache(newsletter_factory):
    newsletter = newsletter_factory(body="first body")
    assert newsletter.body_with_absolute_urls == "first body"

    newsletter.body = "second body"
    assert newsletter.body_with_absolute_urls == "second body"
