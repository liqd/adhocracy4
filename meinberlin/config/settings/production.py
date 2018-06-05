from .base import *

DEBUG = False
# Temporary disable CSP blocking due to CKEditor failures
# CSP_REPORT_ONLY = False
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

# populate settings from RAVEN_CONFIG to LOGGING
raven_config = locals().get('RAVEN_CONFIG', {})
LOGGING['handlers']['sentry'].update(raven_config)
