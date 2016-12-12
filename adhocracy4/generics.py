from django.core.exceptions import ImproperlyConfigured
from django.db import models


def models_to_limit(model_list):
    if len(model_list) < 1:
        raise ImproperlyConfigured('Need at least one model in limit')
    limit_query = models.Q(app_label=model_list[0][0],
                           model=model_list[0][1])
    for model in model_list:
        limit_query = limit_query | models.Q(app_label=model[0],
                                             model=model[1])
    return limit_query
