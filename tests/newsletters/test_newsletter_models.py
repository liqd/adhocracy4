import pytest
from django.conf import settings


@pytest.mark.django_db
def test_absolute_media_urls(newsletter_factory):
    base = 'Relative {rel}test.png' \
           'Tag1: href={rel}test.png' \
           'Tag2: href="{rel}test.png"' \
           "Tag3: href='{rel}test.png'" \
           'Absolute: http://foo.bar/{abs}test.png'

    body = base.format(rel=settings.MEDIA_URL,
                       abs=settings.MEDIA_URL)
    newsletter = newsletter_factory(body=body)

    expected = base.format(rel=settings.BASE_URL + settings.MEDIA_URL,
                           abs=settings.MEDIA_URL)
    assert expected == newsletter.body
