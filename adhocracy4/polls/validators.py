from django.core import exceptions as django_exceptions
from django.utils.translation import gettext as _
from rest_framework import exceptions as rest_exceptions


def single_item_per_module(module, model, pk=None):
    siblings = model.objects.filter(module=module)

    if pk:
        siblings = siblings.exclude(pk=pk)

    if len(siblings) > 0:
        raise django_exceptions.ValidationError(
            {
                django_exceptions.NON_FIELD_ERRORS: [
                    _("Item of type %(item)s for that module already exists")
                    % {"item": model.__name__}
                ]
            }
        )


def question_belongs_to_poll(question, poll_pk):
    if question.poll.pk != poll_pk:
        raise rest_exceptions.ValidationError(
            {
                "question": [
                    _("Question has to belong to the poll set in the url."),
                ]
            }
        )


def choice_belongs_to_question(choice, question_pk):
    if question_pk != choice.question.pk:
        raise rest_exceptions.ValidationError(
            {
                "choice": [
                    _("Choice has to belong to the question set in the url."),
                ]
            }
        )


def single_vote_per_user(user, choice, pk=None):
    from .models import Vote  # avoid circular import

    qs = Vote.objects.filter(choice=choice, creator=user)

    if pk:
        qs = qs.exclude(pk=pk)

    if qs.exists():
        raise django_exceptions.ValidationError(
            {
                "choice": [
                    _("Only one vote per choice is allowed per user."),
                ]
            }
        )
