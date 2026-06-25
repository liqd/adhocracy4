from django.apps import apps


def is_guest_user(user) -> bool:
    """Return whether user is a temporary guest (django-guest-user).

    If django-guest-user is not installed, always returns False.
    """
    if not user.is_authenticated:
        return False
    if not apps.is_installed("guest_user"):
        return False
    try:
        from guest_user.functions import is_guest_user as _is_guest_user
    except ImportError:
        return False
    return _is_guest_user(user)
