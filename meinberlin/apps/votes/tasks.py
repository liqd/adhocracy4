from background_task import background

from adhocracy4.modules.models import Module
from meinberlin.apps.votes.models import VotingToken

BATCH_SIZE = 100000


def generate_voting_tokens(module_id, number_of_tokens):
    number_to_generate = number_of_tokens
    while number_to_generate > 0:
        if number_to_generate >= BATCH_SIZE:
            generate_voting_tokens_batch(module_id, BATCH_SIZE)
            number_to_generate = number_to_generate - BATCH_SIZE
        else:
            generate_voting_tokens_batch(module_id, number_to_generate)
            number_to_generate = 0


@background(schedule=1)
def generate_voting_tokens_batch(module_id, number_of_tokens):
    module = Module.objects.get(pk=module_id)
    VotingToken.objects.bulk_create(
        [VotingToken(module=module) for i in range(number_of_tokens)]
    )
