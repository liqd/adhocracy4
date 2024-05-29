import datetime

import pytest
from django.test.utils import override_settings
from django.utils import translation

from adhocracy4.api.dates import get_date_display
from adhocracy4.api.dates import get_datetime_display

created = datetime.datetime(2022, 7, 1, 17, 0, 0, tzinfo=datetime.timezone.utc)


@pytest.mark.django_db
def test_datetime_display_utc():
    with translation.override("en_EN"):
        datetime_display = get_datetime_display(created)
    assert datetime_display == "July 1, 2022, 5 p.m."


@override_settings(TIME_ZONE="Europe/Berlin")
@pytest.mark.django_db
def test_datetime_display_berlin():
    with translation.override("de_DE"):
        datetime_display = get_datetime_display(created)
    assert datetime_display == "1. Juli 2022, 19:00"


@pytest.mark.django_db
def test_date_display_utc():
    with translation.override("en_EN"):
        date_display = get_date_display(created)
    assert date_display == "July 1, 2022"


@override_settings(TIME_ZONE="Europe/London")
@pytest.mark.django_db
def test_date_display_berlin():
    with translation.override("de_DE"):
        date_display = get_date_display(created)
    assert date_display == "1. Juli 2022"
