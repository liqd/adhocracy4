from pytest_factoryboy import register

from adhocracy4.test.factories import polls as a4_poll_factories

register(a4_poll_factories.PollFactory)
