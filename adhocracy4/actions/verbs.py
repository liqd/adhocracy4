import enum


# http://activitystrea.ms/registry/verbs/
class Verbs(enum.Enum):
    CREATE = 'create'
    ADD = 'add'
    UPDATE = 'update'
    COMPLETE = 'complete'


def choices():
    verbs = list(Verbs)
    return [(verb.value, verb.name) for verb in verbs]
