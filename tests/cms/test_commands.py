import pytest
from dateutil.parser import parse
from django.core.management import call_command

from adhocracy4.projects.enums import Access
from adhocracy4.test.helpers import freeze_phase


@pytest.mark.django_db
def test_update_num_entries(storefront_factory, idea_factory, comment_factory):
    storefront = storefront_factory(num_entries=2)
    assert storefront.num_entries == 2

    idea = idea_factory()
    idea_factory()
    idea_factory()
    comment_factory(content_object=idea)
    comment_factory(content_object=idea)
    comment_factory(content_object=idea)
    comment_factory(content_object=idea)

    call_command("update_storefront_counts")
    storefront.refresh_from_db()
    assert storefront.num_entries == 7


@pytest.mark.django_db
def test_update_num_projects(storefront_factory, phase_factory, plan_factory):
    storefront = storefront_factory(num_projects=1)
    assert storefront.num_projects == 1

    phase_factory(
        start_date=parse("2022-01-01 17:00:00 UTC"),
        end_date=parse("2022-01-31 18:00:00 UTC"),
    )
    phase_23 = phase_factory(
        start_date=parse("2023-01-01 17:00:00 UTC"),
        end_date=parse("2023-01-31 18:00:00 UTC"),
    )
    phase_24 = phase_factory(
        start_date=parse("2024-01-01 17:00:00 UTC"),
        end_date=parse("2024-01-31 18:00:00 UTC"),
    )
    # draft project (not counted)
    phase_24_draft = phase_factory(
        start_date=parse("2024-01-01 17:00:00 UTC"),
        end_date=parse("2024-01-31 18:00:00 UTC"),
    )
    project_draft = phase_24_draft.module.project
    project_draft.is_draft = True
    project_draft.save()
    # semipublic project (counted)
    phase_24_semi = phase_factory(
        start_date=parse("2024-01-01 17:00:00 UTC"),
        end_date=parse("2024-01-31 18:00:00 UTC"),
    )
    project_semi = phase_24_semi.module.project
    project_semi.access = Access.SEMIPUBLIC
    project_semi.save()
    phase_24_private = phase_factory(
        start_date=parse("2024-01-01 17:00:00 UTC"),
        end_date=parse("2024-01-31 18:00:00 UTC"),
    )
    # private project (not counted)
    project_private = phase_24_private.module.project
    project_private.access = Access.PRIVATE
    project_private.save()
    # plans not counted
    plan_factory(status=0)

    with freeze_phase(phase_23):
        call_command("update_storefront_counts")
        storefront.refresh_from_db()
        assert storefront.num_projects == 3

    with freeze_phase(phase_24):
        call_command("update_storefront_counts")
        storefront.refresh_from_db()
        assert storefront.num_projects == 2


@pytest.mark.django_db
def test_update_district_project_count(
    storefront_item_factory,
    phase_factory,
    plan_factory,
    administrative_district_factory,
):
    administrative_district = administrative_district_factory()
    storefront_item = storefront_item_factory(
        district=administrative_district, district_project_count=1
    )
    assert storefront_item.district_project_count == 1

    # project from 22 (not counted as past)
    phase_22 = phase_factory(
        start_date=parse("2022-01-01 17:00:00 UTC"),
        end_date=parse("2022-01-31 18:00:00 UTC"),
    )
    project_22 = phase_22.module.project
    project_22.administrative_district = administrative_district
    project_22.save()
    # project from 23 (only counted when active)
    phase_23 = phase_factory(
        start_date=parse("2023-01-01 17:00:00 UTC"),
        end_date=parse("2023-01-31 18:00:00 UTC"),
    )
    project_23 = phase_23.module.project
    project_23.administrative_district = administrative_district
    project_23.save()
    # project from 24 (counted as future or active)
    phase_24 = phase_factory(
        start_date=parse("2024-01-01 17:00:00 UTC"),
        end_date=parse("2024-01-31 18:00:00 UTC"),
    )
    project_24 = phase_24.module.project
    project_24.administrative_district = administrative_district
    project_24.save()
    # project in future from different district (not counted)
    phase_24_diff_district = phase_factory(
        start_date=parse("2024-01-01 17:00:00 UTC"),
        end_date=parse("2024-01-31 18:00:00 UTC"),
    )
    project_diff_district = phase_24_diff_district.module.project
    different_administrative_district = administrative_district_factory()
    project_diff_district.administrative_district = different_administrative_district
    project_diff_district.save()
    # draft project (not counted)
    phase_24_draft = phase_factory(
        start_date=parse("2024-01-01 17:00:00 UTC"),
        end_date=parse("2024-01-31 18:00:00 UTC"),
    )
    project_draft = phase_24_draft.module.project
    project_draft.is_draft = True
    project_draft.administrative_district = administrative_district
    project_draft.save()
    # semipublic project (counted)
    phase_24_semi = phase_factory(
        start_date=parse("2024-01-01 17:00:00 UTC"),
        end_date=parse("2024-01-31 18:00:00 UTC"),
    )
    project_semi = phase_24_semi.module.project
    project_semi.access = Access.SEMIPUBLIC
    project_semi.administrative_district = administrative_district
    project_semi.save()
    # private project (not counted)
    phase_24_private = phase_factory(
        start_date=parse("2024-01-01 17:00:00 UTC"),
        end_date=parse("2024-01-31 18:00:00 UTC"),
    )
    project_private = phase_24_private.module.project
    project_private.access = Access.PRIVATE
    project_private.administrative_district = administrative_district
    project_private.save()

    # only running plans from same district counted
    plan_factory(status=0, district=administrative_district)
    plan_factory(status=1, district=administrative_district)
    plan_factory(status=0)

    with freeze_phase(phase_23):
        call_command("update_storefront_counts")
        storefront_item.refresh_from_db()
        assert storefront_item.district_project_count == 4

    with freeze_phase(phase_24):
        call_command("update_storefront_counts")
        storefront_item.refresh_from_db()
        assert storefront_item.district_project_count == 3
