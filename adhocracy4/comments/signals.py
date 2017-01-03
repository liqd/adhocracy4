from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_delete

from .models import Comment


def delete_content_object_handler(sender, instance, **kwargs):
    contenttype = ContentType.objects.get_for_model(instance)
    pk = instance.pk
    Comment.objects\
           .filter(content_type=contenttype, object_pk=pk)\
           .delete()


# setup signal handlers for all commentables
for commentable in settings.COMMENTABLES:
    post_delete.connect(
        delete_content_object_handler,
        '.'.join(commentable)
    )
