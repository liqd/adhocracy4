import pytest


@pytest.mark.django_db
def test_str_label(moderation_task):
    assert str(moderation_task) == moderation_task.name
