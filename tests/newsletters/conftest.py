from pytest_factoryboy import register

from meinberlin.apps.test.factories import newsletters

register(newsletters.FollowFactory)
register(newsletters.NewsletterFactory)
