from django.db import models
from django.utils.translation import gettext_lazy as _

from .models import Category


class CategoryField(models.ForeignKey):

    def __init__(self, *args, **kwargs):
        defaults = {
            'verbose_name': _('Category'),
            'to': Category,
            'on_delete': models.SET_NULL,
            'null': True,
            'blank': True,
            'related_name': '+',
        }
        defaults.update(kwargs)
        super().__init__(**defaults)

    def formfield(self, **kwargs):
        from . import forms
        form_class = kwargs.get('form_class', forms.CategoryChoiceField)
        kwargs['form_class'] = form_class
        return super().formfield(**kwargs)
