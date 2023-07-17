import pytest

from meinberlin.apps.bplan.forms import BplanProjectForm


@pytest.mark.django_db
def test_bplan_project_form_metadata_required(organisation, bplan_factory, ImagePNG):
    bplan = bplan_factory(organisation=organisation, tile_image=ImagePNG)
    form = BplanProjectForm(
        instance=bplan,
        data={
            "title": "my changed title",
        },
    )
    assert not form.is_valid()
    assert "tile_image_copyright" in form.errors
    assert "tile_image_alt_text" in form.errors
