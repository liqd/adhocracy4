from .base import *

DEBUG = False
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

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
