from django.db import models

from .models import Category


class CategoryField(models.ForeignKey):

    def __init__(self, *args, **kwargs):
        defaults = {
            'to': Category,
            'on_delete': models.SET_NULL,
            'null': True,
            'blank': True,
            'related_name': '+',
        }
        defaults.update(kwargs)
        super().__init__(**defaults)
