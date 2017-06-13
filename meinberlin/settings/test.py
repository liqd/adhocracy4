from .dev import *

if 'apps.servicekonto.apps.Config' not in INSTALLED_APPS:
    INSTALLED_APPS += ('apps.servicekonto.apps.Config',)

A4_ORGANISATION_FACTORY = 'tests.factories.OrganisationFactory'
A4_USER_FACTORY = 'tests.factories.UserFactory'

ACCOUNT_EMAIL_VERIFICATION = 'optional'
