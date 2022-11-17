from rest_framework.filters import BaseFilterBackend

from meinberlin.apps.moderationtasks.models import ModerationTask


class ModerationTaskFilterBackend(BaseFilterBackend):
    """Filter out proposals that have the moderation tasks completed."""

    def filter_queryset(self, request, queryset, view):

        if 'open_task' in request.GET:
            task_id = request.GET['open_task']
            try:
                moderation_task = ModerationTask.objects.get(id=task_id)
                proposals_completed = getattr(
                    moderation_task,
                    '{app_label}_{model}_completed'.format(
                        app_label=queryset.model._meta.app_label,
                        model=queryset.model.__name__.lower())).all()
                return queryset.exclude(id__in=proposals_completed)
            except ModerationTask.DoesNotExist:
                pass
        return queryset
