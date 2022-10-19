import pytest
from django.conf import settings


@pytest.mark.django_db
def test_absolute_media_urls(platform_email_factory):
    base = 'Relative {rel}test.png' \
           'Tag1: href={rel}test.png' \
           'Tag2: href="{rel}test.png"' \
           "Tag3: href='{rel}test.png'" \
           'Absolute: http://foo.bar/{abs}test.png'

    body = base.format(rel=settings.MEDIA_URL,
                       abs=settings.MEDIA_URL)
    platform_email = platform_email_factory(body=body)

    expected = base.format(
        rel=settings.WAGTAILADMIN_BASE_URL + settings.MEDIA_URL,
        abs=settings.MEDIA_URL)
    assert body == platform_email.body
    assert expected == platform_email.body_with_absolute_urls


@pytest.mark.django_db
def test_invalidate_cache(platform_email_factory):
    platform_email = platform_email_factory(body='first body')
    assert platform_email.body_with_absolute_urls == 'first body'

    platform_email.body = 'second body'
    assert platform_email.body_with_absolute_urls == 'second body'
