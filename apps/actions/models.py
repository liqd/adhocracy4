from django.conf import settings
from django.utils.functional import cached_property

from adhocracy4.actions.models import Action as A4Action

_ACTION_TYPES = {ct: at
                 for at, cts in settings.ACTION_TYPES.items()
                 for ct in cts}


def get_action_type(content_type):
    if hasattr(content_type, 'app_label') and hasattr(content_type, 'model'):
        content_type = (content_type.app_label, content_type.model)
    return _ACTION_TYPES.get(content_type, 'unknown')


class Action(A4Action):
    class Meta:
        proxy = True
        ordering = ('-timestamp',)

    @cached_property
    def type(self):
        return get_action_type(self.obj_content_type)

    @cached_property
    def icon(self):
        if self.type == 'comment':
            return 'comment'
        elif self.type == 'item':
            return 'lightbulb-o'
        elif self.verb == 'add':
            return 'plus'
        elif self.verb == 'update':
            return 'pencil'
        elif self.verb == 'start':
            return 'flag'
        elif self.verb == 'schedule':
            return 'clock-o'
        else:
            return 'star'
