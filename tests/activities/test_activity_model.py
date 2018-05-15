import pytest


@pytest.mark.django_db
def test_activity_url_is_project_url(activity_factory):
    a = activity_factory()
    assert a.get_absolute_url() == a.project.get_absolute_url()


@pytest.mark.django_db
def test_activity_description_removes_script_tag(activity_factory):
    a = activity_factory(description='<script>alert("I love you")</script>')
    assert a.description == 'alert("I love you")'
