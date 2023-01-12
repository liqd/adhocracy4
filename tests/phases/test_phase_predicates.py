import pytest

from adhocracy4.phases import predicates
from adhocracy4.projects.enums import Access
from tests.apps.questions.models import Question
from tests.apps.questions.phases import AskPhase
from tests.apps.questions.phases import RatePhase
from tests.apps.questions.phases import VotePhase
from tests.helpers import active_phase
from tests.helpers import past_phase


@pytest.mark.django_db
def test_has_feature_active_active(question_factory, project_factory):
    project = project_factory(access=Access.PUBLIC)
    question = question_factory(module__project=project)

    with active_phase(question.module, AskPhase):
        assert not predicates.has_feature_active(False, Question, "crud")
        assert predicates.has_feature_active(question.module, Question, "crud")


@pytest.mark.django_db
def test_has_feature_active_past(question_factory, project_factory):
    project = project_factory(access=Access.PUBLIC)
    question = question_factory(module__project=project)

    with past_phase(question.module, AskPhase):
        assert not predicates.has_feature_active(False, Question, "crud")
        assert not predicates.has_feature_active(question.module, Question, "crud")


@pytest.mark.django_db
def test_phase_allows_change_active(
    user_factory, question_factory, project_factory, organisation
):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    organisation.initiators.add(initiator)
    project = project_factory(access=Access.PUBLIC, organisation=organisation)
    question = question_factory(module__project=project)

    with active_phase(question.module, AskPhase):
        assert not predicates.phase_allows_change(user, False)
        assert predicates.phase_allows_change(user, question)
        assert predicates.phase_allows_change(initiator, question)
        assert predicates.phase_allows_change(admin, question)


@pytest.mark.django_db
def test_phase_allows_change_past(
    user_factory, question_factory, project_factory, organisation
):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    organisation.initiators.add(initiator)
    project = project_factory(access=Access.PUBLIC, organisation=organisation)
    question = question_factory(module__project=project)

    with past_phase(question.module, AskPhase):
        assert not predicates.phase_allows_change(user, False)
        assert not predicates.phase_allows_change(user, question)
        assert not predicates.phase_allows_change(initiator, question)
        assert not predicates.phase_allows_change(admin, question)


@pytest.mark.django_db
def test_phase_allows_change_other(
    user_factory, question_factory, project_factory, organisation
):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    organisation.initiators.add(initiator)
    project = project_factory(access=Access.PUBLIC, organisation=organisation)
    question = question_factory(module__project=project)

    with active_phase(question.module, RatePhase):
        assert not predicates.phase_allows_change(user, False)
        assert not predicates.phase_allows_change(user, question)
        assert not predicates.phase_allows_change(initiator, question)
        assert not predicates.phase_allows_change(admin, question)


@pytest.mark.django_db
def test_phase_allows_add_active(
    user_factory, question_factory, project_factory, organisation
):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    organisation.initiators.add(initiator)
    project = project_factory(access=Access.PUBLIC, organisation=organisation)
    question = question_factory(module__project=project)

    with active_phase(question.module, AskPhase):
        assert not predicates.phase_allows_add(Question)(user, False)
        assert predicates.phase_allows_add(Question)(user, question.module)
        assert predicates.phase_allows_add(Question)(initiator, question.module)
        assert predicates.phase_allows_add(Question)(admin, question.module)


@pytest.mark.django_db
def test_phase_allows_add_past(
    user_factory, question_factory, project_factory, organisation
):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    organisation.initiators.add(initiator)
    project = project_factory(access=Access.PUBLIC, organisation=organisation)
    question = question_factory(module__project=project)

    with past_phase(question.module, AskPhase):
        assert not predicates.phase_allows_add(Question)(user, False)
        assert not (predicates.phase_allows_add(Question)(user, question.module))
        assert not (predicates.phase_allows_add(Question)(initiator, question.module))
        assert not (predicates.phase_allows_add(Question)(admin, question.module))


@pytest.mark.django_db
def test_phase_allows_add_other(
    user_factory, question_factory, project_factory, organisation
):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    organisation.initiators.add(initiator)
    project = project_factory(access=Access.PUBLIC, organisation=organisation)
    question = question_factory(module__project=project)

    with active_phase(question.module, RatePhase):
        assert not predicates.phase_allows_add(Question)(user, False)
        assert not (predicates.phase_allows_add(Question)(user, question.module))
        assert not (predicates.phase_allows_add(Question)(initiator, question.module))
        assert not (predicates.phase_allows_add(Question)(admin, question.module))


@pytest.mark.django_db
def test_phase_allows_comment_active(
    user_factory, question_factory, project_factory, organisation
):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    organisation.initiators.add(initiator)
    project = project_factory(access=Access.PUBLIC, organisation=organisation)
    question = question_factory(module__project=project)

    with active_phase(question.module, AskPhase):
        assert not predicates.phase_allows_comment(user, False)
        assert predicates.phase_allows_comment(user, question)
        assert predicates.phase_allows_comment(initiator, question)
        assert predicates.phase_allows_comment(admin, question)


@pytest.mark.django_db
def test_phase_allows_comment_past(
    user_factory, question_factory, project_factory, organisation
):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    organisation.initiators.add(initiator)
    project = project_factory(access=Access.PUBLIC, organisation=organisation)
    question = question_factory(module__project=project)

    with past_phase(question.module, AskPhase):
        assert not predicates.phase_allows_comment(user, False)
        assert not predicates.phase_allows_comment(user, question)
        assert not predicates.phase_allows_comment(initiator, question)
        assert not predicates.phase_allows_comment(admin, question)


@pytest.mark.django_db
def test_phase_allows_comment_other(
    user_factory, question_factory, project_factory, organisation
):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    organisation.initiators.add(initiator)
    project = project_factory(access=Access.PUBLIC, organisation=organisation)
    question = question_factory(module__project=project)

    with active_phase(question.module, RatePhase):
        assert not predicates.phase_allows_comment(user, False)
        assert not predicates.phase_allows_comment(user, question)
        assert not predicates.phase_allows_comment(initiator, question)
        assert not predicates.phase_allows_comment(admin, question)


@pytest.mark.django_db
def test_phase_allows_rate_active(
    user_factory, question_factory, project_factory, organisation
):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    organisation.initiators.add(initiator)
    project = project_factory(access=Access.PUBLIC, organisation=organisation)
    question = question_factory(module__project=project)

    with active_phase(question.module, RatePhase):
        assert not predicates.phase_allows_rate(user, False)
        assert predicates.phase_allows_rate(user, question)
        assert predicates.phase_allows_rate(initiator, question)
        assert predicates.phase_allows_rate(admin, question)


@pytest.mark.django_db
def test_phase_allows_rate_past(
    user_factory, question_factory, project_factory, organisation
):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    organisation.initiators.add(initiator)
    project = project_factory(access=Access.PUBLIC, organisation=organisation)
    question = question_factory(module__project=project)

    with past_phase(question.module, RatePhase):
        assert not predicates.phase_allows_rate(user, False)
        assert not predicates.phase_allows_rate(user, question)
        assert not predicates.phase_allows_rate(initiator, question)
        assert not predicates.phase_allows_rate(admin, question)


@pytest.mark.django_db
def test_phase_allows_rate_other(
    user_factory, question_factory, project_factory, organisation
):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    organisation.initiators.add(initiator)
    project = project_factory(access=Access.PUBLIC, organisation=organisation)
    question = question_factory(module__project=project)

    with active_phase(question.module, AskPhase):
        assert not predicates.phase_allows_rate(user, False)
        assert not predicates.phase_allows_rate(user, question)
        assert not predicates.phase_allows_rate(initiator, question)
        assert not predicates.phase_allows_rate(admin, question)


@pytest.mark.django_db
def test_phase_allows_vote_active(
    user_factory, question_factory, project_factory, organisation
):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    organisation.initiators.add(initiator)
    project = project_factory(access=Access.PUBLIC, organisation=organisation)
    question = question_factory(module__project=project)

    with active_phase(question.module, VotePhase):
        assert not predicates.phase_allows_vote(user, False)
        assert predicates.phase_allows_vote(user, question)
        assert predicates.phase_allows_vote(initiator, question)
        assert predicates.phase_allows_vote(admin, question)


@pytest.mark.django_db
def test_phase_allows_vote_past(
    user_factory, question_factory, project_factory, organisation
):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    organisation.initiators.add(initiator)
    project = project_factory(access=Access.PUBLIC, organisation=organisation)
    question = question_factory(module__project=project)

    with past_phase(question.module, VotePhase):
        assert not predicates.phase_allows_vote(user, False)
        assert not predicates.phase_allows_vote(user, question)
        assert not predicates.phase_allows_vote(initiator, question)
        assert not predicates.phase_allows_vote(admin, question)


@pytest.mark.django_db
def test_phase_allows_vote_other(
    user_factory, question_factory, project_factory, organisation
):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    organisation.initiators.add(initiator)
    project = project_factory(access=Access.PUBLIC, organisation=organisation)
    question = question_factory(module__project=project)

    with active_phase(question.module, AskPhase):
        assert not predicates.phase_allows_vote(user, False)
        assert not predicates.phase_allows_vote(user, question)
        assert not predicates.phase_allows_vote(initiator, question)
        assert not predicates.phase_allows_vote(admin, question)


@pytest.mark.django_db
def test_phase_allows_delete_vote_active(
    user_factory, question_factory, project_factory, organisation, token_vote_factory
):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    organisation.initiators.add(initiator)
    project = project_factory(access=Access.PUBLIC, organisation=organisation)
    question = question_factory(module__project=project)
    token_vote = token_vote_factory(content_object=question)

    with active_phase(question.module, VotePhase):
        assert not predicates.phase_allows_delete_vote(user, False)
        assert predicates.phase_allows_delete_vote(user, token_vote)
        assert predicates.phase_allows_delete_vote(initiator, token_vote)
        assert predicates.phase_allows_delete_vote(admin, token_vote)


@pytest.mark.django_db
def test_phase_allows_delete_vote_past(
    user_factory, question_factory, project_factory, organisation, token_vote_factory
):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    organisation.initiators.add(initiator)
    project = project_factory(access=Access.PUBLIC, organisation=organisation)
    question = question_factory(module__project=project)
    token_vote = token_vote_factory(content_object=question)

    with past_phase(question.module, VotePhase):
        assert not predicates.phase_allows_delete_vote(user, False)
        assert not predicates.phase_allows_delete_vote(user, token_vote)
        assert not predicates.phase_allows_delete_vote(initiator, token_vote)
        assert not predicates.phase_allows_delete_vote(admin, token_vote)


@pytest.mark.django_db
def test_phase_allows_delete_vote_other(
    user_factory, question_factory, project_factory, organisation, token_vote_factory
):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    organisation.initiators.add(initiator)
    project = project_factory(access=Access.PUBLIC, organisation=organisation)
    question = question_factory(module__project=project)
    token_vote = token_vote_factory(content_object=question)

    with active_phase(question.module, AskPhase):
        assert not predicates.phase_allows_delete_vote(user, False)
        assert not predicates.phase_allows_delete_vote(user, token_vote)
        assert not predicates.phase_allows_delete_vote(initiator, token_vote)
        assert not predicates.phase_allows_delete_vote(admin, token_vote)


@pytest.mark.django_db
def test_phase_allows_add_vote_active(
    user_factory, question_factory, project_factory, organisation
):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    organisation.initiators.add(initiator)
    project = project_factory(access=Access.PUBLIC, organisation=organisation)
    question = question_factory(module__project=project)

    with active_phase(question.module, VotePhase):
        assert not predicates.phase_allows_add_vote(Question)(user, False)
        assert predicates.phase_allows_add_vote(Question)(user, question.module)
        assert predicates.phase_allows_add_vote(Question)(initiator, question.module)
        assert predicates.phase_allows_add_vote(Question)(admin, question.module)


@pytest.mark.django_db
def test_phase_allows_add_vote_past(
    user_factory, question_factory, project_factory, organisation
):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    organisation.initiators.add(initiator)
    project = project_factory(access=Access.PUBLIC, organisation=organisation)
    question = question_factory(module__project=project)

    with past_phase(question.module, VotePhase):
        assert not predicates.phase_allows_add_vote(Question)(user, False)
        assert not (predicates.phase_allows_add_vote(Question)(user, question.module))
        assert not (
            predicates.phase_allows_add_vote(Question)(initiator, question.module)
        )
        assert not (predicates.phase_allows_add_vote(Question)(admin, question.module))


@pytest.mark.django_db
def test_phase_allows_add_vote_other(
    user_factory, question_factory, project_factory, organisation
):
    user = user_factory()
    admin = user_factory(is_superuser=True)
    initiator = user_factory()
    organisation.initiators.add(initiator)
    project = project_factory(access=Access.PUBLIC, organisation=organisation)
    question = question_factory(module__project=project)

    with active_phase(question.module, RatePhase):
        assert not predicates.phase_allows_add_vote(Question)(user, False)
        assert not (predicates.phase_allows_add_vote(Question)(user, question.module))
        assert not (
            predicates.phase_allows_add_vote(Question)(initiator, question.module)
        )
        assert not (predicates.phase_allows_add_vote(Question)(admin, question.module))
