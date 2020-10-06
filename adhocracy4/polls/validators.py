from django.core.exceptions import NON_FIELD_ERRORS
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


def single_item_per_module(module, model, pk=None):
    siblings = model.objects.filter(module=module)

    if pk:
        siblings = siblings.exclude(pk=pk)

    if len(siblings) > 0:
        raise ValidationError({
            NON_FIELD_ERRORS: [
                _('Item of type %(item)s for that module already exists') % {
                    'item': model.__name__
                }]
        })


def single_vote_per_user(user, choice, pk=None):
    from .models import Vote  # avoid circular import

    if choice.question.multiple_choice:
        # Allow multiple votes per user for multiple choice questions.
        return

    qs = Vote.objects\
        .filter(choice__question=choice.question)\
        .filter(creator=user)

    if pk:
        qs = qs.exclude(pk=pk)

    if qs.exists():
        raise ValidationError({
            NON_FIELD_ERRORS: [
                _('Only one vote per question is allowed per user.'),
            ]
        })


def choice_belongs_to_question(choice, question_pk):
    if question_pk != choice.question.pk:
        raise ValidationError({
            NON_FIELD_ERRORS: [
                _('Choice has to belong to the question set in the url.'),
            ]
        })
