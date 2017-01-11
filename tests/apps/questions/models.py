from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from adhocracy4.modules.models import Item
from adhocracy4.comments.models import Comment


class Question(Item):
    text = models.CharField(max_length=120,
                            default='Can i haz cheezburger, pls?')

    comments = GenericRelation(Comment,
                               related_query_name='question',
                               object_id_field='object_pk')
