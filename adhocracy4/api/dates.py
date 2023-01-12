from django.template import defaultfilters
from django.utils import timezone


def get_datetime_display(datetime):
    """Convert datetime instance to localtime and return as str."""
    local_datetime = timezone.localtime(datetime)
    local_date = defaultfilters.date(local_datetime)
    local_time = defaultfilters.time(local_datetime)

    return local_date + ", " + local_time


def get_date_display(datetime):
    """Convert datetime instance to localtime and return date as str."""
    local_datetime = timezone.localtime(datetime)
    local_date = defaultfilters.date(local_datetime)

    return local_date
