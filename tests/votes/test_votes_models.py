import pytest
from django.core.exceptions import ValidationError
from django.utils import translation

from meinberlin.apps.votes.models import TokenVote


@pytest.mark.django_db
def test_voting_token_str(voting_token):
    voting_token_string = voting_token.__str__()
    assert voting_token_string == "{}-{}-{}-{}".format(
        voting_token.token[0:4],
        voting_token.token[4:8],
        voting_token.token[8:12],
        voting_token.token[12:16],
    )


@pytest.mark.django_db
def test_voting_token_project(voting_token):
    assert voting_token.module.project == voting_token.project


@pytest.mark.django_db
def test_token_vote_save(module_factory, proposal_factory, voting_token_factory):
    module = module_factory()
    other_module = module_factory()
    proposal = proposal_factory(module=module)
    token = voting_token_factory(module=module, is_active=False)
    other_token = voting_token_factory(module=other_module)

    with pytest.raises(ValidationError) as error:
        TokenVote.objects.create(content_object=proposal, token=other_token)
    with translation.override("en_GB"):
        assert error.value.messages[0] == "This token is not valid for this project."
    assert TokenVote.objects.all().count() == 0

    with pytest.raises(ValidationError) as error:
        TokenVote.objects.create(content_object=proposal, token=token)
    with translation.override("en_GB"):
        assert error.value.messages[0] == "This token is not active."
    assert TokenVote.objects.all().count() == 0

    token.is_active = True
    token.save()

    TokenVote.objects.create(content_object=proposal, token=token)
    assert TokenVote.objects.all().count() == 1

    for i in range(4):
        proposal_tmp = proposal_factory(module=module)
        TokenVote.objects.create(content_object=proposal_tmp, token=token)
    assert TokenVote.objects.all().count() == 5

    proposal_tmp = proposal_factory(module=module)
    with pytest.raises(ValidationError) as error:
        TokenVote.objects.create(content_object=proposal_tmp, token=token)
    with translation.override("en_GB"):
        assert error.value.messages[0] == "This token has no votes left."
    assert TokenVote.objects.all().count() == 5
