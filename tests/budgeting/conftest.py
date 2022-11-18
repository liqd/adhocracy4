from pytest_factoryboy import register

from meinberlin.test.factories import ModerationTaskFactory
from meinberlin.test.factories import budgeting
from meinberlin.test.factories import votes

register(budgeting.ProposalFactory)
register(ModerationTaskFactory)
register(votes.TokenVoteFactory)
register(votes.VotingTokenFactory)
