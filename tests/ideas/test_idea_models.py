import pytest
from django.core.urlresolvers import reverse


@pytest.mark.django_db
def test_absolute_url(idea):
    url = reverse('idea-detail', kwargs={'slug': idea.slug})
    assert idea.get_absolute_url() == url


@pytest.mark.django_db
def test_save(idea):
    assert '<script>' not in idea.description


@pytest.mark.django_db
def test_str(idea):
    idea_string = idea.__str__()
    assert idea_string == idea.name


@pytest.mark.django_db
def test_project(idea):
    assert idea.module.project == idea.project
