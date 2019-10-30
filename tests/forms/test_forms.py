import pytest
from dateutil.parser import parse
from django import forms

from adhocracy4.forms.fields import DateTimeField


class DateTimeForm(forms.Form):
    date = DateTimeField(
        time_format='%H:%M',
        required=False,
        require_all_fields=False,
    )


@pytest.mark.django_db
def test_datetimefield_valid(user):
    data = {'date_0': '2023-01-01', 'date_1': '12:30'}
    form = DateTimeForm(data=data)
    assert form.is_valid()
    assert form.cleaned_data['date'] == \
        parse('2023-01-01 12:30:00 UTC')


@pytest.mark.django_db
def test_datetimefield_invalid(user):
    data = {'date_0': 'not a date', 'date_1': '12:30'}
    form = DateTimeForm(data=data)
    assert not form.is_valid()


@pytest.mark.django_db
def test_datetimefield_empty_none(user):
    data = {'date_0': '', 'date_1': ''}
    form = DateTimeForm(data=data)
    assert form.is_valid()
    assert form.cleaned_data['date'] is None


@pytest.mark.django_db
def test_datetimefield_default_time(user):
    data = {'date_0': '2023-01-01', 'date_1': ''}
    form = DateTimeForm(data=data)
    assert form.is_valid()
    assert form.cleaned_data['date'] == \
        parse('2023-01-01 00:00:00 UTC')
