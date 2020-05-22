from pytest_factoryboy import register

from meinberlin.test.factories import newsletters
from meinberlin.test.factories import platformemails

register(newsletters.EmailAddressFactory)
register(platformemails.PlatformEmailFactory)
