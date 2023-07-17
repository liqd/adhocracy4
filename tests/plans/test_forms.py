import pytest

from meinberlin.apps.plans.forms import PlanForm


@pytest.mark.django_db
def test_plan_form_metadata_required(organisation, plan_factory, ImagePNG):
    plan = plan_factory(organisation=organisation, image=ImagePNG, tile_image=ImagePNG)
    form = PlanForm(
        instance=plan,
        data={
            "title": "my changed title",
        },
    )
    assert not form.is_valid()
    assert "image_copyright" in form.errors
    assert "image_alt_text" in form.errors
    assert "tile_image_copyright" in form.errors
    assert "tile_image_alt_text" in form.errors
