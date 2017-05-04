from django.core.exceptions import NON_FIELD_ERRORS
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from adhocracy4.modules import models as module_models

from . import models


def item_belongs_to_module(module, item):
    if type(module) in (int, str):
        module = module_models.Module.objects.get(pk=module)

    if item.module != module:
        raise ValidationError({
            NON_FIELD_ERRORS: [
                _('Item has to belong to the module defined in the url.'),
            ]
        })


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
