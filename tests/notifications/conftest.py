from pytest_factoryboy import register

from meinberlin.test.factories import budgeting as budgeting_factories
from meinberlin.test.factories import offlineevents

register(budgeting_factories.ProposalFactory)
register(offlineevents.OfflineEventFactory)
