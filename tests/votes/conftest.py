from pytest_factoryboy import register

from meinberlin.test.factories import budgeting as budgeting_factories
from meinberlin.test.factories import votes as votes_factories

register(budgeting_factories.ProposalFactory)
register(votes_factories.TokenVoteFactory)
register(votes_factories.VotingTokenFactory)
