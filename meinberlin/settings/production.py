from .base import *

COMPRESS = True
COMPRESS_OFFLINE = True

DEBUG = False

try:
    from .local import *
except ImportError:
    pass
