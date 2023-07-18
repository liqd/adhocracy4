import pytest

from adhocracy4.test.helpers import render_template


@pytest.mark.django_db
def test_project_tile_image(project):
    template = "{% load project_tags %}" "{% project_tile_image project as x %}{{x}}"

    project.image = "image"
    project.tile_image = "tileimage"
    assert "tileimage" == render_template(template, {"project": project})

    project.tile_image = ""
    assert "image" == render_template(template, {"project": project})

    project.image = ""
    assert "None" == render_template(template, {"project": project})


@pytest.mark.django_db
def test_project_tile_image_copyright(project):
    template = (
        "{% load project_tags %}" "{% project_tile_image_copyright project as x %}{{x}}"
    )

    project.image = "image"
    project.image_copyright = "image_copyright"
    project.tile_image = "tileimage"
    project.tile_image_copyright = "tileimage_copyright"
    assert "tileimage_copyright" == render_template(template, {"project": project})

    project.tile_image = ""
    assert "image_copyright" == render_template(template, {"project": project})

    project.image = ""
    assert "None" == render_template(template, {"project": project})


@pytest.mark.django_db
def test_project_tile_image_alt_text(project):
    template = (
        "{% load project_tags %}" "{% project_tile_image_alt_text project as x %}{{x}}"
    )

    project.image = "image"
    project.image_alt_text = "image_alt_text"
    project.tile_image = "tileimage"
    project.tile_image_alt_text = "tileimage_alt_text"
    assert "tileimage_alt_text" == render_template(template, {"project": project})

    project.tile_image = ""
    assert "image_alt_text" == render_template(template, {"project": project})

    project.image = ""
    assert "None" == render_template(template, {"project": project})
