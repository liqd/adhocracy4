from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


def single_document_per_module(module, pk=None):
    from .models import Document
    siblings = Document.objects.filter(module=module)

    if pk:
        siblings = siblings.exclude(pk=pk)

    if len(siblings) != 0:
        raise ValidationError(
            _('Document for that module already exists')
        )
