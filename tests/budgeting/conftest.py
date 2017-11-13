from pytest_factoryboy import register

from meinberlin.apps.test.factories import budgeting

register(budgeting.ProposalFactory)
