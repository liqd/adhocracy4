from pytest_factoryboy import register

from meinberlin.test.factories import budgeting
from meinberlin.test.factories import ideas

from . import factories as invites

register(invites.ModeratorInviteFactory)
register(invites.ParticipantInviteFactory)
register(ideas.IdeaFactory)
register(budgeting.ProposalFactory)
