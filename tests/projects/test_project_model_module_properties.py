import pytest
from dateutil.parser import parse
from freezegun import freeze_time


@pytest.mark.django_db
def test_running_modules(project, module_factory, phase_factory):
    module1 = module_factory(project=project, weight=1)
    module2 = module_factory(project=project, weight=2)
    module3 = module_factory(project=project, weight=3)
    module4 = module_factory(project=project, weight=4)
    phase_factory(
        module=module1,
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:05:00 UTC')
    )
    phase_factory(
        module=module1,
        start_date=parse('2013-01-01 19:00:00 UTC'),
        end_date=parse('2013-01-01 19:05:00 UTC')
    )
    phase_factory(
        module=module2,
        start_date=parse('2013-01-01 17:05:00 UTC'),
        end_date=parse('2013-01-01 19:00:00 UTC')
    )
    phase_factory(
        module=module3,
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:05:00 UTC')
    )
    phase_factory(
        module=module4,
        start_date=parse('2013-01-01 19:05:00 UTC'),
        end_date=parse('2013-01-01 20:00:00 UTC')
    )
    with freeze_time('2013-01-01 18:30:00 UTC'):
        assert module1 in project.running_modules
        assert module1 in project.modules
        assert module2 in project.running_modules
        assert module2 in project.modules
        assert module3 not in project.running_modules
        assert module3 in project.modules
        assert module4 not in project.running_modules
        assert module4 in project.modules


@pytest.mark.django_db
def test_running_module_ends_next(project, module_factory, phase_factory):
    module1 = module_factory(project=project, weight=1)
    module2 = module_factory(project=project, weight=2)
    phase_factory(
        module=module1,
        start_date=parse('2013-01-01 17:05:00 UTC'),
        end_date=parse('2013-01-01 18:05:00 UTC')
    )
    phase_factory(
        module=module1,
        start_date=parse('2013-01-01 19:00:00 UTC'),
        end_date=parse('2013-01-01 19:05:00 UTC')
    )
    phase_factory(
        module=module2,
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 19:10:00 UTC')
    )
    with freeze_time('2013-01-01 18:30:00 UTC'):
        assert module1 == project.running_module_ends_next


@pytest.mark.django_db
def test_past_modules(project, module_factory, phase_factory):
    module1 = module_factory(project=project, weight=1)
    module2 = module_factory(project=project, weight=2)
    module3 = module_factory(project=project, weight=3)
    module4 = module_factory(project=project, weight=4)
    phase_factory(
        module=module1,
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:05:00 UTC')
    )
    phase_factory(
        module=module1,
        start_date=parse('2013-01-01 19:00:00 UTC'),
        end_date=parse('2013-01-01 19:05:00 UTC')
    )
    phase_factory(
        module=module2,
        start_date=parse('2013-01-01 17:05:00 UTC'),
        end_date=parse('2013-01-01 19:00:00 UTC')
    )
    phase_factory(
        module=module3,
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:05:00 UTC')
    )
    phase_factory(
        module=module4,
        start_date=parse('2013-01-01 19:10:00 UTC'),
        end_date=parse('2013-01-01 20:00:00 UTC')
    )
    with freeze_time('2013-01-01 19:06:00 UTC'):
        assert module1 in project.past_modules
        assert module2 in project.past_modules
        assert module3 in project.past_modules
        assert module4 not in project.past_modules


@pytest.mark.django_db
def test_future_modules(project, module_factory, phase_factory):
    module1 = module_factory(project=project, weight=1)
    module2 = module_factory(project=project, weight=2)
    module3 = module_factory(project=project, weight=3)
    module4 = module_factory(project=project, weight=4)
    phase_factory(
        module=module1,
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:05:00 UTC')
    )
    phase_factory(
        module=module1,
        start_date=parse('2013-01-01 19:00:00 UTC'),
        end_date=parse('2013-01-01 19:05:00 UTC')
    )
    phase_factory(
        module=module2,
        start_date=parse('2013-01-01 17:05:00 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )
    phase_factory(
        module=module3,
        start_date=parse('2013-01-01 19:00:00 UTC'),
        end_date=parse('2013-01-01 20:05:00 UTC')
    )
    phase_factory(
        module=module4,
        start_date=parse('2013-01-01 19:05:00 UTC'),
        end_date=parse('2013-01-01 20:00:00 UTC')
    )
    with freeze_time('2013-01-01 18:30:00 UTC'):
        assert module1 not in project.future_modules
        assert module2 not in project.future_modules
        assert module3 in project.future_modules
        assert module4 in project.future_modules


@pytest.mark.django_db
def test_module_running_days_left(project, module_factory, phase_factory):
    module1 = module_factory(project=project, weight=1)
    module2 = module_factory(project=project, weight=2)
    phase_factory(
        module=module1,
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:05:00 UTC')
    )
    phase_factory(
        module=module1,
        start_date=parse('2013-01-01 19:00:00 UTC'),
        end_date=parse('2013-01-02 19:05:00 UTC')
    )
    phase_factory(
        module=module2,
        start_date=parse('2013-01-01 17:05:00 UTC'),
        end_date=parse('2013-01-05 19:00:00 UTC')
    )
    with freeze_time('2013-01-01 18:30:00 UTC'):
        assert project.module_running_days_left == 1


@pytest.mark.django_db
def test_module_running_time_left(project_factory, module_factory,
                                  phase_factory):
    project = project_factory()
    module1 = module_factory(project=project, weight=1)
    phase_factory(
        module=module1,
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:05:00 UTC')
    )
    phase_factory(
        module=module1,
        start_date=parse('2013-01-01 19:00:00 UTC'),
        end_date=parse('2013-01-02 19:05:00 UTC')
    )
    project2 = project_factory()
    module2 = module_factory(project=project2, weight=1)
    phase_factory(
        module=module2,
        start_date=parse('2013-01-01 18:00:00 UTC'),
        end_date=parse('2013-01-01 18:30:00.45 UTC')
    )
    with freeze_time('2013-01-01 18:30:00 UTC'):
        assert project.module_running_time_left == '1 day'
        assert project2.module_running_time_left == '0 seconds'


@pytest.mark.django_db
def test_module_running_progress(project, module_factory, phase_factory):
    module1 = module_factory(project=project, weight=1)
    phase_factory(
        module=module1,
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:05:00 UTC')
    )
    phase_factory(
        module=module1,
        start_date=parse('2013-01-01 19:00:00 UTC'),
        end_date=parse('2013-01-02 19:05:00 UTC')
    )
    with freeze_time('2013-01-01 18:30:00 UTC'):
        assert project.module_running_progress == 6


@pytest.mark.django_db
def test_module_not_running_time_left(project, module_factory, phase_factory):
    module1 = module_factory(project=project, weight=1)
    phase_factory(
        module=module1,
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:05:00 UTC')
    )
    phase_factory(
        module=module1,
        start_date=parse('2013-01-01 19:00:00 UTC'),
        end_date=parse('2013-01-02 19:05:00 UTC')
    )
    with freeze_time('2013-01-02 19:30:00 UTC'):
        assert project.module_running_time_left is None
        assert project.module_running_days_left is None
        assert project.module_running_progress is None


@pytest.mark.django_db
def test_published_modules(project, module_factory):
    module1 = module_factory(project=project, weight=1, is_draft=True)
    module2 = module_factory(project=project, weight=2)
    assert module1 in project.modules
    assert module1 not in project.published_modules
    assert module1 in project.unpublished_modules
    assert module2 in project.modules
    assert module2 in project.published_modules
    assert module2 not in project.unpublished_modules
