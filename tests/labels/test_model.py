import pytest


@pytest.mark.django_db
def test_str_label(label):
    assert str(label) == label.name
