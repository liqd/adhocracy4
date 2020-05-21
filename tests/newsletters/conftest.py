from pytest_factoryboy import register

from meinberlin.test.factories import newsletters

register(newsletters.FollowFactory)
register(newsletters.NewsletterFactory)
register(newsletters.EmailAddressFactory)
