import os
from urllib.parse import urlparse

from django.conf import settings
from django.core.urlresolvers import resolve
from easy_thumbnails.files import get_thumbnailer


def createThumbnail(imagefield):
    thumbnailer = get_thumbnailer(imagefield)
    thumbnail = thumbnailer.generate_thumbnail(
        {'size': (800, 400), 'crop': 'smart'})
    thumbnailer.save_thumbnail(thumbnail)
    thumbnail_path = os.path.join(settings.MEDIA_ROOT, thumbnail.path)
    return thumbnail_path


def templates_used(response):
    if not hasattr(response, 'templates'):
        raise Exception("Response wasn't render from template")
    names = [template.name for template in response.templates]
    return names


def redirect_target(response):
    if response.status_code not in [301, 302]:
        raise Exception("Response wasn't a redirect")
    location = urlparse(response['location'])
    return resolve(location.path).url_name
