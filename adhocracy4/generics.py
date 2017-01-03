from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models.signals import post_delete

"""
Helpers to use generic foreign keys.

Most of the helper accept a list of models, it should contain tuples of app
and model names.
"""


def models_to_limit(model_list):
    """
    Creates limit query for content type foreign key from list of models.
    """

    if len(model_list) < 1:
        raise ImproperlyConfigured('Need at least one model in limit')
    limit_query = models.Q(app_label=model_list[0][0],
                           model=model_list[0][1])
    for model in model_list:
        limit_query = limit_query | models.Q(app_label=model[0],
                                             model=model[1])
    return limit_query


def setup_delete_signals(model_list, generic_model):
    """
    Ensure that generic model instance is deleted if content object was.
    """
    def delete_content_object_handler(sender, instance, **kwargs):
        contenttype = ContentType.objects.get_for_model(instance)
        pk = instance.pk
        generic_model.objects\
                     .filter(content_type=contenttype, object_pk=pk)\
                     .delete()

    for model in model_list:
        post_delete.connect(
            delete_content_object_handler,
            '.'.join(model),
            weak=False
        )
