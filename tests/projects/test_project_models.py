import os
from datetime import timedelta

import pytest
from dateutil.parser import parse
from django.conf import settings
from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from freezegun import freeze_time

from adhocracy4.projects import models
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
@pytest.mark.parametrize('project__is_public', [False])
def test_is_privat(project):
    assert not project.is_public
    assert project.is_private


@pytest.mark.django_db
def test_no_days_left(phase):
    project = phase.module.project
    with freeze_time(phase.end_date):
        assert project.days_left is None


@pytest.mark.django_db
def test_one_day_left(phase):
    project = phase.module.project
    with freeze_time(phase.end_date - timedelta(days=1)):
        assert project.days_left == 1


@pytest.mark.django_db
def test_has_finished(phase):
    project = phase.module.project
    with freeze_time(phase.end_date + timedelta(days=1)):
        assert project.days_left is None
        assert project.has_finished is True


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
    assert 'Image must be at least 600 pixels high' in str(e)


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
def test_phases_property(module, phase_factory):
    project = module.project
    phase1 = phase_factory(module=module, type='fake:30:type', weight=30)
    phase2 = phase_factory(module=module, type='fake:20:type', weight=20)

    assert list(project.phases) == [phase2, phase1]


@pytest.mark.django_db
def test_future_phases_property(module, phase_factory):
    project = module.project
    phase1 = phase_factory(
        module=module,
        start_date=parse('2013-03-01 18:00:00 UTC'),
        end_date=parse('2013-03-02 18:00:00 UTC')
    )
    phase2 = phase_factory(
        module=module,
        start_date=parse('2013-02-01 18:00:00 UTC'),
        end_date=parse('2013-02-02 18:00:00 UTC')
    )
    phase3 = phase_factory(
        module=module,
        start_date=parse('2013-01-01 18:00:00 UTC'),
        end_date=parse('2013-01-02 18:00:00 UTC')
    )
    phase4 = phase_factory(
        module=module,
        start_date=None,
        end_date=None
    )

    with freeze_time(phase3.start_date):
        assert list(project.future_phases) == [phase4, phase2, phase1]
    with freeze_time(phase3.end_date):
        assert list(project.future_phases) == [phase4, phase2, phase1]
    with freeze_time(phase2.start_date):
        assert list(project.future_phases) == [phase4, phase1]
    with freeze_time(phase2.end_date):
        assert list(project.future_phases) == [phase4, phase1]


@pytest.mark.django_db
def test_past_phases_property(module, phase_factory):
    project = module.project
    phase_factory(
        module=module,
        start_date=parse('2013-03-01 18:00:00 UTC'),
        end_date=parse('2013-03-02 18:00:00 UTC')
    )
    phase2 = phase_factory(
        module=module,
        start_date=parse('2013-02-01 18:00:00 UTC'),
        end_date=parse('2013-02-02 18:00:00 UTC')
    )
    phase3 = phase_factory(
        module=module,
        start_date=parse('2013-01-01 18:00:00 UTC'),
        end_date=parse('2013-01-02 18:00:00 UTC')
    )

    with freeze_time(phase3.start_date):
        assert list(project.past_phases) == []
    with freeze_time(phase3.end_date):
        assert list(project.past_phases) == [phase3]
    with freeze_time(phase2.start_date):
        assert list(project.past_phases) == [phase3]
    with freeze_time(phase2.end_date):
        assert list(project.past_phases) == [phase2, phase3]


@pytest.mark.django_db
def test_active_module_property(project, module_factory, phase_factory):
    module = module_factory(project=project, weight=2)
    module2 = module_factory(project=project, weight=1)
    phase_factory(
        module=module,
        start_date=parse('2013-03-01 18:00:00 UTC'),
        end_date=parse('2013-03-02 18:00:00 UTC')
    )
    phase2 = phase_factory(
        module=module,
        start_date=parse('2013-01-05 18:00:00 UTC'),
        end_date=parse('2013-01-12 18:00:00 UTC')
    )
    phase3 = phase_factory(
        module=module2,
        start_date=parse('2013-01-01 18:00:00 UTC'),
        end_date=parse('2013-01-10 18:00:00 UTC')
    )

    with freeze_time(phase3.start_date - timedelta(minutes=1)):
        assert project.active_module is None
    with freeze_time(phase3.start_date):
        assert project.active_module == module2
    with freeze_time(phase2.start_date):
        assert project.active_module == module2
    with freeze_time(phase2.end_date - timedelta(minutes=1)):
        assert project.active_module == module
    with freeze_time(phase2.end_date):
        assert project.active_module is None
