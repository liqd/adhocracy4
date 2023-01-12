import pytest

from adhocracy4.test.helpers import render_template


def test_get_days_tag():
    template = "{% load project_tags %}{% get_days days as x %}{{x}}"

    assert "a few hours left" == render_template(template, {"days": 0})
    assert "1 day left" == render_template(template, {"days": 1})
    assert "2 days left" == render_template(template, {"days": 2})


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
