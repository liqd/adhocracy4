from django.core.exceptions import NON_FIELD_ERRORS
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from . import models


def single_item_per_module(module, model, pk=None):
    siblings = model.objects.filter(module=module)

    if pk:
        siblings = siblings.exclude(pk=pk)

    if len(siblings) != 0:
        raise ValidationError(
            _('Item of type %(item)s for that module already exists') % {
                'item': model.__name__
            }
        )


def single_vote_per_user(user, question, pk=None):
    qs = models.Vote.objects\
        .filter(choice__question=question)\
        .filter(creator=user)

    if pk:
        qs = qs.exclude(pk=pk)

    if len(qs) > 0:
        raise ValidationError({
            NON_FIELD_ERRORS: [
                _('Only one vote per question is allowed per user.'),
            ]
        })
