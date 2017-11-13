from .dev import *

if 'meinberlin.apps.servicekonto.apps.Config' not in INSTALLED_APPS:
    INSTALLED_APPS += ('meinberlin.apps.servicekonto.apps.Config',)

A4_ORGANISATION_FACTORY = \
    'meinberlin.apps.test.factories.OrganisationFactory'
A4_USER_FACTORY = 'meinberlin.apps.test.factories.UserFactory'

ACCOUNT_EMAIL_VERIFICATION = 'optional'
