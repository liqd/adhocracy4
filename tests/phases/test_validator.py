import pytest
from django.core import exceptions

from adhocracy4.phases import validators


def test_validator_with_testapp():
    validated = validators.validate_content('a4test_questions:020:ask')
    assert validated == 'a4test_questions:020:ask'


def test_validator_invalid_phase():
    with pytest.raises(exceptions.ValidationError):
        validators.validate_content('noapp:020:nophase')
