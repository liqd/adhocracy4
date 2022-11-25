from pytest_factoryboy import register

from meinberlin.test.factories.budgeting import ProposalFactory

from .factories import ModerationTaskFactory

register(ModerationTaskFactory)
register(ProposalFactory)
