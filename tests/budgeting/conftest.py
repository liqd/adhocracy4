from pytest_factoryboy import register

from meinberlin.test.factories import budgeting
from meinberlin.test.factories import votes

register(budgeting.ProposalFactory)
register(votes.VotingTokenFactory)
