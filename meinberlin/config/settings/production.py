from .base import *

COMPRESS = True
COMPRESS_OFFLINE = True
STATICFILES_STORAGE = 'meinberlin.apps.contrib.staticfiles.NonStrictManifestStaticFilesStorage'

DEBUG = False

try:
    from .local import *
except ImportError:
    pass

try:
    from .polygons import *
except ImportError:
    pass

try:
    INSTALLED_APPS += tuple(ADDITIONAL_APPS)
except NameError:
    pass
