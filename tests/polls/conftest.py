from pytest_factoryboy import register

from meinberlin.test.factories import polls

register(polls.PollFactory)
