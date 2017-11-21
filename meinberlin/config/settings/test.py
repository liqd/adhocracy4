from .dev import *

if 'meinberlin.apps.servicekonto.apps.Config' not in INSTALLED_APPS:
    INSTALLED_APPS += ('meinberlin.apps.servicekonto.apps.Config',)

A4_ORGANISATION_FACTORY = \
    'meinberlin.test.factories.organisations.OrganisationFactory'
A4_USER_FACTORY = 'meinberlin.test.factories.UserFactory'

ACCOUNT_EMAIL_VERIFICATION = 'optional'
