from pytest_factoryboy import register

from . import factories as invites

register(invites.ModeratorInviteFactory)
register(invites.ParticipantInviteFactory)
