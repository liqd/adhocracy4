from django.utils.functional import cached_property

from adhocracy4.actions.models import Action


ACTIVITY_TYPES = {
    'project': [
        ('a4projects', 'project'),
        ('meinberlin_bplan', 'bplan'),
        ('meinberlin_externalproject', 'externalproject'),
    ],
    'phase': [
        ('a4phases', 'phase'),
    ],
    'comment': [
        ('a4comments', 'comment'),
    ],
    'rating': [
        ('a4ratings', 'rating'),
    ],
    'item': [
        ('meinberlin_budgeting', 'proposal'),
        ('meinberlin_ideas', 'idea'),
        ('meinberlin_kiezkasse', 'proposal'),
        ('meinberlin_mapideas', 'mapidea'),
    ]
}

_ACTIVITY_TYPES = {ct: at for at, cts in ACTIVITY_TYPES.items() for ct in cts}


def get_activity_type(content_type):
    if hasattr(content_type, 'app_label') and hasattr(content_type, 'model'):
        content_type = (content_type.app_label, content_type.model)
    return _ACTIVITY_TYPES.get(content_type, 'unknown')


class Activity(Action):
    class Meta:
        proxy = True
        ordering = ('-timestamp',)

    @cached_property
    def type(self):
        return get_activity_type(self.obj_content_type)
