from django.contrib.auth.decorators import user_passes_test

from meinberlin.apps.organisations.models import Organisation


def user_is_project_admin(view_func):
    """Projet admin view decorator.

    Checks that the user is an admin, initiator or project group member
    of any project.
    """
    return user_passes_test(
        _user_is_project_admin,
    )(view_func)


def _user_is_project_admin(user):
    is_group_member = user.groups.exists()
    is_initiator = Organisation.objects.filter(initiators__id=user.id).exists()
    return user.is_active and \
        (user.is_superuser or is_initiator or is_group_member)
