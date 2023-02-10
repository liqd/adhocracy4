import pytest

from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.ideas import phases


@pytest.mark.django_db
def test_storefront_str(storefront):
    assert str(storefront) == storefront.title


@pytest.mark.django_db
def test_storefront_num_entries(storefront_factory, idea, comment_factory):
    comment_factory(content_object=idea)
    comment_factory(content_object=idea)
    storefront = storefront_factory()
    assert storefront.num_entries == 3


@pytest.mark.django_db
def test_storefront_num_projects(
    storefront_factory, project_factory, plan_factory, phase_factory
):
    phase, _, _, _ = setup_phase(phase_factory, None, phases.CollectPhase)
    project_factory()
    plan_factory(status=0)
    with freeze_phase(phase):
        storefront = storefront_factory()
    assert storefront.num_projects == 1


@pytest.mark.django_db
def test_storefront_item_str(storefront_item):
    assert str(storefront_item) == str(storefront_item.pk)


@pytest.mark.django_db
def test_storefront_item_district_project_count(
    storefront_item_factory,
    project_factory,
    plan_factory,
    phase_factory,
    administrative_district,
):
    phase, _, project, _ = setup_phase(phase_factory, None, phases.CollectPhase)
    project.administrative_district = administrative_district
    project.save()
    project_factory(administrative_district=administrative_district)
    plan_factory(status=0, district=administrative_district)
    with freeze_phase(phase):
        storefront_item = storefront_item_factory(district=administrative_district)
    assert storefront_item.district_project_count == 2


@pytest.mark.django_db
def test_storefront_item_item_type(storefront_item_factory, project, external_project):
    project_storefront_item = storefront_item_factory(project=project)
    external_project_storefront_item = storefront_item_factory(project=external_project)
    assert project_storefront_item.item_type == "project"
    assert external_project_storefront_item.item_type == "external"


@pytest.mark.django_db
def test_storefront_item_project_url(
    storefront_item_factory, project, external_project
):
    project_storefront_item = storefront_item_factory(project=project)
    external_project_storefront_item = storefront_item_factory(project=external_project)
    assert project_storefront_item.project_url == project.get_absolute_url()
    assert (
        external_project_storefront_item.project_url
        == external_project.externalproject.url
    )
