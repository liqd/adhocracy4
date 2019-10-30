from .test import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'postgres',
        'NAME': 'django',
        'TEST': {
            'NAME': 'django_test'
        },
    }
}
