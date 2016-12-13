from django.core import exceptions

from . import content


def validate_content(identifier):
    if identifier not in content:
        raise exceptions.ValidationError('Specify a valid phase name')
    return identifier
