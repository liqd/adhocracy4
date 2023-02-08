from background_task import background

from adhocracy4.modules.models import Module
from meinberlin.apps.votes.models import VotingToken
from meinberlin.apps.votes.models import get_token_12

# Number of tokens to insert into database per bulk_create
BATCH_SIZE = 100
# Max number of tokens in one download / package
PACKAGE_SIZE = 100


def generate_voting_tokens(module_id, number_of_tokens, existing_tokens):
    module = Module.objects.get(pk=module_id)
    package_number = VotingToken.next_package_number(module)
    module_name = module.name
    project_id = module.project.id
    project_name = module.project.name

    number_to_generate = number_of_tokens
    package_number_limit = 0
    if number_of_tokens > PACKAGE_SIZE:
        package_number_limit = number_of_tokens - PACKAGE_SIZE
    while number_to_generate > 0:
        if number_to_generate >= BATCH_SIZE:
            generate_voting_tokens_batch(
                module_id,
                BATCH_SIZE,
                package_number,
                number_of_tokens,
                module_name,
                project_id,
                project_name,
                existing_tokens,
            )
            number_to_generate = number_to_generate - BATCH_SIZE
        else:
            generate_voting_tokens_batch(
                module_id,
                number_to_generate,
                package_number,
                number_of_tokens,
                module_name,
                project_id,
                project_name,
                existing_tokens,
            )
            number_to_generate = 0
        if package_number_limit >= number_to_generate:
            package_number += 1
            package_number_limit - PACKAGE_SIZE


@background(schedule=1)
def generate_voting_tokens_batch(
    module_id,
    batch_size,
    package_number,
    number_of_tokens,
    module_name,
    project_id,
    project_name,
    existing_tokens,
):
    module = Module.objects.get(pk=module_id)
    VotingToken.objects.bulk_create(
        [get_token_and_hash(module, package_number) for i in range(batch_size)]
    )


def get_token_and_hash(module, package_number):
    token = get_token_12()
    token_hash = VotingToken.hash_token(token, module)
    return VotingToken(
        token=token, token_hash=token_hash, module=module, package_number=package_number
    )
