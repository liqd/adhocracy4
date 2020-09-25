from .settings import *  # noqa: F403, F401

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
