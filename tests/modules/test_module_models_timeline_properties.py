import pytest
from dateutil.parser import parse


@pytest.mark.django_db
def test_project_modules(module_factory, project):

    module = module_factory(project=project)
    module_factory(project=project)
    module_factory(project=project)
    module_factory(project=project)

    assert module.project_modules.count() == 4
    assert module.other_modules.count() == 3


@pytest.mark.django_db
def test_is_in_cluster_one_module(module_factory, project):

    module = module_factory(project=project)
    assert not module.is_in_module_cluster
    assert module.index_in_cluster is None
    assert module.readable_index_in_cluster is None
    assert len(module.module_cluster) == 0
    assert not module.next_module_in_cluster
    assert not module.previous_module_in_cluster
    assert module.get_timeline_index == 0
    assert module.get_detail_url == \
        module.project.get_absolute_url()


@pytest.mark.django_db
def test_is_in_cluster_overlapping_module(
        phase_factory, module_factory, project):

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

    phase_factory(
        module=module2,
        start_date=parse('2013-01-15 17:00:00 UTC'),
        end_date=parse('2013-02-15 18:05:00 UTC')
    )

    assert module1.is_in_module_cluster
    assert module2.is_in_module_cluster

    assert module1.index_in_cluster == 0
    assert module2.index_in_cluster == 1

    assert module1.readable_index_in_cluster == 1
    assert module2.readable_index_in_cluster == 2

    assert len(module1.module_cluster) == 2
    assert len(module2.module_cluster) == 2

    assert module1.next_module_in_cluster == module2
    assert not module1.previous_module_in_cluster

    assert not module2.next_module_in_cluster
    assert module2.previous_module_in_cluster == module1

    assert module1.get_timeline_index == 0
    assert module2.get_timeline_index == 0

    assert module1.get_detail_url == \
        module1.get_absolute_url()
    assert module2.get_detail_url == \
        module2.get_absolute_url()


@pytest.mark.django_db
def test_is_in_cluster_overlapping_module_and_timeline(
        phase_factory, module_factory, project):

    module1 = module_factory(project=project)
    module2 = module_factory(project=project)
    module3 = module_factory(project=project)

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

    phase_factory(
        module=module2,
        start_date=parse('2013-01-15 17:00:00 UTC'),
        end_date=parse('2013-02-15 18:05:00 UTC')
    )

    phase_factory(
        module=module3,
        start_date=parse('2013-03-04 17:00:00 UTC'),
        end_date=parse('2013-03-05 18:05:00 UTC')
    )

    assert module1.is_in_module_cluster
    assert module2.is_in_module_cluster
    assert not module3.is_in_module_cluster

    assert module1.index_in_cluster == 0
    assert module2.index_in_cluster == 1
    assert module3.index_in_cluster == 0

    assert module1.readable_index_in_cluster == 1
    assert module2.readable_index_in_cluster == 2
    assert module3.readable_index_in_cluster == 1

    assert len(module1.module_cluster) == 2
    assert len(module2.module_cluster) == 2
    assert len(module3.module_cluster) == 1

    assert module1.next_module_in_cluster == module2
    assert not module1.previous_module_in_cluster

    assert not module2.next_module_in_cluster
    assert module2.previous_module_in_cluster == module1

    assert not module3.next_module_in_cluster
    assert not module3.previous_module_in_cluster

    assert module1.get_timeline_index == 0
    assert module2.get_timeline_index == 0
    assert module3.get_timeline_index == 1

    assert module1.get_detail_url == \
        module1.get_absolute_url()
    assert module2.get_detail_url == \
        module2.get_absolute_url()
    assert module3.get_detail_url == \
        '{}?initialSlide={}'.format(module3.project.get_absolute_url(),
                                    module3.get_timeline_index)
