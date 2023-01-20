from django_filters import rest_framework as rest_filters

from meinberlin.apps.moderationtasks.models import ModerationTask


class OpenTaskFilter(rest_filters.ModelChoiceFilter):
    """
    Filter out proposals that have the moderation tasks completed.

    Works like a negative label filter.
    """

    def filter(self, queryset, value):
        try:
            proposals_completed = getattr(
                value,
                "{app_label}_{model}_completed".format(
                    app_label=queryset.model._meta.app_label,
                    model=queryset.model.__name__.lower(),
                ),
            ).all()
            return queryset.exclude(id__in=proposals_completed)
        except AttributeError:
            pass
        except ModerationTask.DoesNotExist:
            pass
        return queryset
