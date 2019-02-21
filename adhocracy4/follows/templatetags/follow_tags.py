from django import template

from .. import models

register = template.Library()


@register.simple_tag()
def is_following(user, project):
    return (
        user.is_authenticated and
        models.Follow.objects.filter(
            enabled=True,
            project=project,
            creator=user
        ).exists()
    )
