import pytest
from dateutil.parser import parse
from freezegun import freeze_time


@pytest.mark.django_db
def test_module_cluster(phase_factory, module_factory, project):

    module1 = module_factory(project=project)
    module2 = module_factory(project=project)

    phase1 = phase_factory(
        module=module1,
        start_date=parse("2013-01-01 17:00:00 UTC"),
        end_date=parse("2013-01-13 18:05:00 UTC"),
    )

    phase_factory(
        module=module1,
        start_date=parse("2013-01-12 17:00:00 UTC"),
        end_date=parse("2013-02-01 18:05:00 UTC"),
    )

    phase3 = phase_factory(
        module=module1,
        start_date=parse("2013-02-02 17:00:00 UTC"),
        end_date=parse("2013-03-03 8:05:00 UTC"),
    )

    assert str(module1.module_start) == "2013-01-01 17:00:00+00:00"
    assert str(module1.module_end) == "2013-03-03 08:05:00+00:00"

    phase_factory(
        module=module2,
        start_date=parse("2013-01-15 17:00:00 UTC"),
        end_date=parse("2013-02-15 18:05:00 UTC"),
    )

    assert len(project.module_clusters) == 1
    assert len(project.module_cluster_dict) == 1

    assert project.module_clusters[0][0] == module1
    assert project.module_clusters[0][1] == module2

    assert project.module_cluster_dict[0]["date"] == phase1.start_date
    assert project.module_cluster_dict[0]["end_date"] == phase3.end_date


@pytest.mark.django_db
def test_time_line(phase_factory, module_factory, project):

    module1 = module_factory(project=project)
    module2 = module_factory(project=project)

    phase_factory(
        module=module1,
        start_date=parse("2013-01-01 17:00:00 UTC"),
        end_date=parse("2013-01-13 18:05:00 UTC"),
    )

    phase_factory(
        module=module1,
        start_date=parse("2013-01-12 17:00:00 UTC"),
        end_date=parse("2013-02-01 18:05:00 UTC"),
    )

    phase_factory(
        module=module1,
        start_date=parse("2013-02-02 17:00:00 UTC"),
        end_date=parse("2013-03-03 8:05:00 UTC"),
    )

    assert str(module1.module_start) == "2013-01-01 17:00:00+00:00"
    assert str(module1.module_end) == "2013-03-03 08:05:00+00:00"

    phase_factory(
        module=module2,
        start_date=parse("2013-05-05 17:00:00 UTC"),
        end_date=parse("2013-06-06 18:05:00 UTC"),
    )

    assert len(project.module_clusters) == 2
    assert len(project.module_cluster_dict) == 2

    assert len(project.participation_dates) == 2
    assert project.display_timeline
    assert not project.get_current_participation_date()

    with freeze_time("2013-05-10 18:30:00 UTC"):
        assert project.get_current_participation_date() == 1

    with freeze_time("2013-01-12 18:05:00 UTC"):
        assert project.get_current_participation_date() == 0
