# http://activitystrea.ms/registry/verbs/

CREATE = 'created'
ADD = 'added'
UPDATE = 'updated'
COMPLETE = 'completed'


def all():
    items = sorted(globals().items())
    return [(value, name) for name, value in items
            if not name.startswith('_') and name != 'all']
