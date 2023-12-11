import os

import pytest
from dateutil.parser import parse
from django.conf import settings
from django.test.utils import override_settings
from django.urls import reverse
from freezegun import freeze_time

from adhocracy4.projects import models
from adhocracy4.projects.enums import Access
from adhocracy4.test import helpers


@pytest.mark.django_db
def test_get_by_natural_key(project):
    assert project == models.Project.objects.get_by_natural_key(project.name)


@pytest.mark.django_db
def test_str(project):
    assert str(project) == project.name


@pytest.mark.django_db
def test_get_absolute_url(project):
    project_url = reverse("project-detail", args=[project.slug])
    assert project.get_absolute_url() == project_url


@override_settings(ALLOWED_UPLOAD_IMAGES=("image/jpeg"))
@pytest.mark.django_db
def test_image_validation_image_too_small(project_factory, image_factory):
    project = project_factory(image=image_factory((200, 200)))
    with pytest.raises(Exception) as e:
        project.full_clean()
    assert "Image must be at least 600 pixels high" in str(e.value)


@override_settings(ALLOWED_UPLOAD_IMAGES=("image/jpeg"))
@pytest.mark.django_db
def test_image_big_enough(project_factory, image_factory):
    project = project_factory(image=image_factory((1400, 1400)))
    assert project.full_clean() is None


@override_settings(ALLOWED_UPLOAD_IMAGES=("image/jpeg"))
@pytest.mark.django_db
def test_delete_project(project_factory, image_factory):
    project = project_factory(image=image_factory((1400, 1400), "PNG"))
    image_path = os.path.join(settings.MEDIA_ROOT, project.image.path)
    thumbnail_path = helpers.create_thumbnail(project.image)
    assert os.path.isfile(thumbnail_path)
    assert os.path.isfile(image_path)
    count = models.Project.objects.all().count()
    assert count == 1
    project.delete()
    assert not os.path.isfile(thumbnail_path)
    assert not os.path.isfile(image_path)
    count = models.Project.objects.all().count()
    assert count == 0


@pytest.mark.django_db
def test_image_deleted_after_update(project_factory, image_factory):
    project = project_factory(image=image_factory((1440, 1400)))
    image_path = os.path.join(settings.MEDIA_ROOT, project.image.path)
    thumbnail_path = helpers.create_thumbnail(project.image)

    assert os.path.isfile(image_path)
    assert os.path.isfile(thumbnail_path)

    project.image = None
    project.save()

    assert not os.path.isfile(image_path)
    assert not os.path.isfile(thumbnail_path)


# FIXME: add tests for has_member, is_group_member, and has_moderator


@pytest.mark.django_db
def test_feature_projects(project_factory):
    projects = [project_factory(is_draft=False) for i in range(10)]
    featured = list(models.Project.objects.featured())
    assert featured == list(reversed(projects))[:8]


# project properties
# FIXME: add tests for topic names


@pytest.mark.django_db
def test_other_projects(organisation, project_factory):
    project = project_factory(organisation=organisation)
    related_project = project_factory(organisation=organisation)
    assert list(project.other_projects) == [related_project]


@pytest.mark.django_db
@pytest.mark.parametrize("project__access", [Access.PRIVATE])
def test_is_private(project):
    assert not project.is_public
    assert project.is_private
    assert not project.is_semipublic


@pytest.mark.django_db
def test_is_public(project):
    assert project.is_public
    assert not project.is_private
    assert not project.is_semipublic


@pytest.mark.django_db
@pytest.mark.parametrize("project__access", [Access.SEMIPUBLIC])
def test_is_semipublic(project):
    assert not project.is_public
    assert not project.is_private
    assert project.is_semipublic


@pytest.mark.django_db
def test_is_archivable(project_factory, phase_factory):
    project1 = project_factory(is_archived=True)
    project2 = project_factory(is_archived=False)
    project3 = project_factory(is_archived=False)
    phase_factory(
        start_date=parse("2013-01-01 18:00:00 UTC"),
        end_date=parse("2013-01-01 19:00:00 UTC"),
        module__project=project1,
    )
    phase_factory(
        start_date=parse("2013-01-01 18:00:00 UTC"),
        end_date=parse("2013-01-01 19:00:00 UTC"),
        module__project=project2,
    )
    phase_factory(
        start_date=parse("2013-01-01 18:00:00 UTC"),
        end_date=parse("2013-01-01 18:25:00 UTC"),
        module__project=project3,
    )
    with freeze_time(parse("2013-01-01 18:30:00 UTC")):
        assert not project1.is_archivable
        assert not project2.is_archivable
        assert project3.is_archivable


@pytest.mark.django_db
def test_project_topics(project_factory, topic_factory):
    project = project_factory()
    assert project.topic_names == []
    # delete to clear the cache of the cached_property
    del project.topic_names
    topic1 = topic_factory(projects=[project])
    assert project.topic_names == [str(topic1)]
    # delete to clear the cache of the cached_property
    del project.topic_names
    topic2 = topic_factory(projects=[project])
    assert project.topic_names == [str(topic1), str(topic2)]
