from django.core.exceptions import ValidationError

from django.utils.translation import ugettext as _


def single_poll_per_module(module, pk=None):
    from .models import Poll
    siblings = Poll.objects.filter(module=module)

    if pk:
        siblings = siblings.exclude(pk=pk)

    if len(siblings) != 0:
        raise ValidationError(
            _('Document for that module already exists')
        )


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

