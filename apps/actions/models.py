from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

from adhocracy4.actions.models import Action as A4Action
from adhocracy4.actions.verbs import Verbs

_ACTION_TYPES = {ct: at
                 for at, cts in settings.ACTION_TYPES.items()
                 for ct in cts}


def get_action_type(content_type):
    if hasattr(content_type, 'app_label') and hasattr(content_type, 'model'):
        content_type = (content_type.app_label, content_type.model)
    return _ACTION_TYPES.get(content_type, 'unknown')


class ActionQuerySet(models.QuerySet):
    def public(self):
        return self.filter(
            (models.Q(project__is_draft=False) &
             models.Q(project__is_public=True)) |
            models.Q(project__isnull=True))

    def exclude_updates(self):
        return self.exclude(verb=Verbs.UPDATE.value)


class Action(A4Action):
    class Meta:
        proxy = True
        ordering = ('-timestamp',)

    objects = ActionQuerySet.as_manager()

    @cached_property
    def type(self):
        return get_action_type(self.obj_content_type)

    @cached_property
    def icon(self):
        if self.type == 'comment':
            return 'comment'
        elif self.type == 'item':
            return 'lightbulb-o'
        elif self.verb == Verbs.ADD.value:
            return 'plus'
        elif self.verb == Verbs.UPDATE.value:
            return 'pencil'
        elif self.verb == Verbs.START.value:
            return 'flag'
        elif self.verb == Verbs.SCHEDULE.value:
            return 'clock-o'
        else:
            return 'star'

    @staticmethod
    def proxy_of(action):
        """Cast an A4Action object to the proxied Action."""
        assert action.__class__ == A4Action
        action.__class__ = Action
        return action
