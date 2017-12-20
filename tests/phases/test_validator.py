import pytest
from django.core import exceptions

from adhocracy4.phases import validators


def test_validator_with_testapp():
    validated = validators.validate_content('a4test_questions:ask')
    assert validated == 'a4test_questions:ask'


def test_validator_invalid_phase():
    with pytest.raises(exceptions.ValidationError):
        validators.validate_content('noapp:nophase')
