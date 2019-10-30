from django.apps import apps
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test

from adhocracy4.projects.models import Project

Organisation = apps.get_model(settings.A4_ORGANISATIONS_MODEL)


def user_is_project_admin(view_func):
    """Projet admin view decorator.

    Checks that the user is an admin, moderator or initiator of any project.
    """
    return user_passes_test(
        _user_is_project_admin,
    )(view_func)


def _user_is_project_admin(user):
    is_moderator = Project.objects.filter(moderators__id=user.id).exists()
    is_initiator = Organisation.objects.filter(initiators__id=user.id).exists()
    return user.is_active and \
        (user.is_superuser or is_initiator or is_moderator)
