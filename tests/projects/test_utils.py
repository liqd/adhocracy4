import pytest
from dateutil.parser import parse

from adhocracy4.modules.models import Module
from adhocracy4.phases.models import Phase
from adhocracy4.projects.utils import get_module_clusters
from adhocracy4.projects.utils import get_module_clusters_dict


@pytest.mark.django_db
def test_module_cluster_mixin_modules_overlapping(
        phase_factory, module_factory):

    module1 = module_factory()
    module2 = module_factory()

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
        start_date=parse('2013-01-15 17:00:00 UTC'),
        end_date=parse('2013-02-15 18:05:00 UTC')
    )

    modules = Module.objects.annotate_module_start().annotate_module_end()
    module_clusters = get_module_clusters(modules)
    module_cluster_dict = get_module_clusters_dict(module_clusters)

    assert len(module_clusters) == 1
    assert len(module_cluster_dict) == 1

    start_date = Phase.objects.all().order_by('start_date').first().start_date
    end_date = Phase.objects.all().order_by('end_date').last().end_date

    assert module_clusters[0][0].module_start == start_date
    assert module_cluster_dict[0]['date'] == start_date
    assert module_cluster_dict[0]['end_date'] == end_date


@pytest.mark.django_db
def test_module_cluster_mixin_modules_successively(
        phase_factory, module_factory):

    module1 = module_factory()
    module2 = module_factory()

    phase_factory(
        module=module1,
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-13 18:05:00 UTC')
    )

    phase_factory(
        module=module2,
        start_date=parse('2013-01-15 17:00:00 UTC'),
        end_date=parse('2013-02-01 18:05:00 UTC')
    )

    assert str(module1.module_start) == '2013-01-01 17:00:00+00:00'
    assert str(module1.module_end) == '2013-01-13 18:05:00+00:00'

    assert str(module2.module_start) == '2013-01-15 17:00:00+00:00'
    assert str(module2.module_end) == '2013-02-01 18:05:00+00:00'

    modules = Module.objects.annotate_module_start().annotate_module_end()
    module_clusters = get_module_clusters(modules)

    assert len(module_clusters) == 2


@pytest.mark.django_db
def test_module_cluster_mixin_modules_same_time(phase_factory, module_factory):

    module1 = module_factory()
    module2 = module_factory()

    phase_factory(
        module=module1,
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-13 18:05:00 UTC')
    )

    phase_factory(
        module=module2,
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-13 18:05:00 UTC')
    )

    assert str(module1.module_start) == '2013-01-01 17:00:00+00:00'
    assert str(module1.module_end) == '2013-01-13 18:05:00+00:00'

    assert str(module2.module_start) == '2013-01-01 17:00:00+00:00'
    assert str(module2.module_end) == '2013-01-13 18:05:00+00:00'

    modules = Module.objects.annotate_module_start().annotate_module_end()
    module_clusters = get_module_clusters(modules)

    assert len(module_clusters) == 1

    start_date = Phase.objects.all().order_by('start_date').first().start_date
    end_date = Phase.objects.all().order_by('end_date').last().end_date

    assert module_clusters[0][0].module_start == start_date
    assert module_clusters[0][0].module_end == end_date

    assert module_clusters[0][1].module_start == start_date
    assert module_clusters[0][1].module_end == end_date
