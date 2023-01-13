import pytest


@pytest.mark.django_db
def test_project(moderator_remark):
    assert moderator_remark.project == moderator_remark.item.project


@pytest.mark.django_db
def test_content(moderator_remark):
    assert moderator_remark.content
    moderator_remark.remark = ""
    moderator_remark.save()
    assert not moderator_remark.content
