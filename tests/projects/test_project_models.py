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
def test_get_absolute_url(project):
    project_url = reverse('project-detail', args=[project.slug])
    assert project.get_absolute_url() == project_url


@pytest.mark.django_db
def test_get_by_natural_key(project):
    assert project == models.Project.objects.get_by_natural_key(project.name)


@pytest.mark.django_db
def test_is_public(project):
    assert project.is_public
    assert not project.is_private


@pytest.mark.django_db
@pytest.mark.parametrize('project__access', [Access.PRIVATE])
def test_is_private(project):
    assert not project.is_public
    assert project.is_private


@pytest.mark.django_db
def test_str(project):
    assert str(project) == project.name


@pytest.mark.django_db
def test_feature_projects(project_factory):
    projects = [project_factory(is_draft=False) for i in range(10)]
    featured = list(models.Project.objects.featured())
    assert featured == list(reversed(projects))[:8]


@pytest.mark.django_db
def test_other_projects(organisation, project_factory):
    project = project_factory(organisation=organisation)
    related_project = project_factory(organisation=organisation)
    assert list(project.other_projects) == [related_project]


@override_settings(ALLOWED_UPLOAD_IMAGES=('image/jpeg'))
@pytest.mark.django_db
def test_image_validation_image_too_small(project_factory, image_factory):
    project = project_factory(image=image_factory((200, 200)))
    with pytest.raises(Exception) as e:
        project.full_clean()
    assert 'Image must be at least 600 pixels high' in str(e.value)


@override_settings(ALLOWED_UPLOAD_IMAGES=('image/jpeg'))
@pytest.mark.django_db
def test_image_big_enough(project_factory, image_factory):
    project = project_factory(image=image_factory((1400, 1400)))
    assert project.full_clean() is None


@override_settings(ALLOWED_UPLOAD_IMAGES=('image/jpeg'))
@pytest.mark.django_db
def test_delete_project(project_factory, image_factory):
    project = project_factory(image=image_factory((1400, 1400), 'PNG'))
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


@pytest.mark.django_db
def test_is_archivable(project_factory, phase_factory):
    project1 = project_factory(is_archived=True)
    project2 = project_factory(is_archived=False)
    project3 = project_factory(is_archived=False)
    phase_factory(
        start_date=parse('2013-01-01 18:00:00 UTC'),
        end_date=parse('2013-01-01 19:00:00 UTC'),
        module__project=project1,
    )
    phase_factory(
        start_date=parse('2013-01-01 18:00:00 UTC'),
        end_date=parse('2013-01-01 19:00:00 UTC'),
        module__project=project2,
    )
    phase_factory(
        start_date=parse('2013-01-01 18:00:00 UTC'),
        end_date=parse('2013-01-01 18:25:00 UTC'),
        module__project=project3,
    )
    with freeze_time(parse('2013-01-01 18:30:00 UTC')):
        assert not project1.is_archivable
        assert not project2.is_archivable
        assert project3.is_archivable


@pytest.mark.django_db
def test_module_cluster(phase_factory, module_factory, project):

    module1 = module_factory(project=project)
    module2 = module_factory(project=project)

    phase1 = phase_factory(
        module=module1,
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-13 18:05:00 UTC')
    )

    phase_factory(
        module=module1,
        start_date=parse('2013-01-12 17:00:00 UTC'),
        end_date=parse('2013-02-01 18:05:00 UTC')
    )

    phase3 = phase_factory(
        module=module1,
        start_date=parse('2013-02-02 17:00:00 UTC'),
        end_date=parse('2013-03-03 8:05:00 UTC')
    )

    assert str(module1.module_start) == '2013-01-01 17:00:00+00:00'
    assert str(module1.module_end) == '2013-03-03 08:05:00+00:00'

    phase_factory(
        module=module2,
        start_date=parse('2013-01-15 17:00:00 UTC'),
        end_date=parse('2013-02-15 18:05:00 UTC')
    )

    assert len(project.module_clusters) == 1
    assert len(project.module_cluster_dict) == 1

    assert project.module_clusters[0][0] == module1
    assert project.module_clusters[0][1] == module2

    assert project.module_cluster_dict[0]['date'] == phase1.start_date
    assert project.module_cluster_dict[0]['end_date'] == phase3.end_date


@pytest.mark.django_db
def test_time_line(phase_factory, module_factory, project):

    module1 = module_factory(project=project)
    module2 = module_factory(project=project)

    phase_factory(
        module=module1,
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-13 18:05:00 UTC')
    )

    phase_factory(
        module=module1,
        start_date=parse('2013-01-12 17:00:00 UTC'),
        end_date=parse('2013-02-01 18:05:00 UTC')
    )

    phase_factory(
        module=module1,
        start_date=parse('2013-02-02 17:00:00 UTC'),
        end_date=parse('2013-03-03 8:05:00 UTC')
    )

    assert str(module1.module_start) == '2013-01-01 17:00:00+00:00'
    assert str(module1.module_end) == '2013-03-03 08:05:00+00:00'

    phase_factory(
        module=module2,
        start_date=parse('2013-05-05 17:00:00 UTC'),
        end_date=parse('2013-06-06 18:05:00 UTC')
    )

    assert len(project.module_clusters) == 2
    assert len(project.module_cluster_dict) == 2

    assert len(project.participation_dates) == 2
    assert project.display_timeline
    assert not project.get_current_participation_date()

    with freeze_time('2013-05-10 18:30:00 UTC'):
        assert project.get_current_participation_date() == 1

    with freeze_time('2013-01-12 18:05:00 UTC'):
        assert project.get_current_participation_date() == 0
