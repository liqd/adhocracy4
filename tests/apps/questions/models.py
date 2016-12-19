from django.db import models

from adhocracy4.modules.models import Item


class Question(Item):
    text = models.CharField(max_length=120,
                            default='Can i haz cheezburger, pls?')
