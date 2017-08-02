
from pytest_factoryboy import register

from . import factories

register(factories.FollowFactory)
register(factories.NewsletterFactory)
