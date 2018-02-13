"""WSGI WhiteNoise config for meinberlin project."""

import os

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meinberlin.config.settings")

application = get_wsgi_application()

application = WhiteNoise(application)
application.add_files(settings.STATIC_ROOT, settings.STATIC_URL)
application.add_files(settings.MEDIA_ROOT, settings.MEDIA_URL)
