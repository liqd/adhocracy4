from celery import shared_task

from adhocracy4.modules.models import Module
from meinberlin.apps.votes.models import TokenPackage
from meinberlin.apps.votes.models import VotingToken
from meinberlin.apps.votes.models import get_token_16

# Number of tokens to insert into database per bulk_create
BATCH_SIZE = int(1e5)
# Max number of tokens in one download / package
PACKAGE_SIZE = int(1e6)


def generate_voting_tokens(module_id, number_of_tokens):
    module = Module.objects.get(pk=module_id)

    number_to_generate = number_of_tokens
    # determine when to go to next package_number
    package_number_limit = 0
    package_size = number_of_tokens
    if number_of_tokens > PACKAGE_SIZE:
        package_number_limit = number_of_tokens - PACKAGE_SIZE
        package_size = PACKAGE_SIZE
    package = TokenPackage.objects.create(module=module, size=package_size)

    while number_to_generate > 0:
        if number_to_generate >= BATCH_SIZE:
            generate_voting_tokens_batch.delay(
                module_id,
                BATCH_SIZE,
                package.pk,
            )
            number_to_generate = number_to_generate - BATCH_SIZE
        else:
            generate_voting_tokens_batch.delay(
                module_id,
                number_to_generate,
                package.pk,
            )
            number_to_generate = 0
        if package_number_limit > 0 and package_number_limit >= number_to_generate:
            package_number_limit = package_number_limit - PACKAGE_SIZE
            if package_number_limit < PACKAGE_SIZE:
                package_size = number_to_generate
            package = TokenPackage.objects.create(module=module, size=package_size)


@shared_task
def generate_voting_tokens_batch(
    module_id,
    batch_size,
    package_id,
):
    module = Module.objects.get(pk=module_id)
    package = TokenPackage.objects.get(pk=package_id)
    VotingToken.objects.bulk_create(
        [get_token_and_hash(module, package) for i in range(batch_size)]
    )


def get_token_and_hash(module, package):
    token = get_token_16()
    token_hash = VotingToken.hash_token(token, module)
    return VotingToken(
        token=token, token_hash=token_hash, module=module, package=package
    )


@shared_task
def delete_plain_codes(package_pk):
    queryset = VotingToken.objects.filter(package__pk=package_pk)
    queryset.update(token="")
