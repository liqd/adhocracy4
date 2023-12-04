import factory
import pytest

from adhocracy4.test.helpers import render_template


@pytest.mark.django_db
def test_project_url(project, external_project_factory, bplan_factory):
    external_project = external_project_factory(url=factory.Faker("url"))
    bplan = bplan_factory(url=factory.Faker("url"))
    template = "{% load meinberlin_project_tags %}" "{{ project|project_url }}"

    assert project.get_absolute_url() == render_template(template, {"project": project})
    assert external_project.externalproject.url == render_template(
        template, {"project": external_project}
    )
    assert bplan.externalproject.url == render_template(template, {"project": bplan})


@pytest.mark.django_db
def test_is_external(project, external_project, bplan):
    template = (
        "{% load meinberlin_project_tags %}"
        "{% if project|is_external %}"
        "is external"
        "{% else %}"
        "is not external"
        "{% endif %}"
    )

    assert "is not external" == render_template(template, {"project": project})
    assert "is external" == render_template(template, {"project": external_project})
    assert "is external" == render_template(template, {"project": bplan})


@pytest.mark.django_db
def test_is_a4_project(project, external_project, bplan):
    template = (
        "{% load meinberlin_project_tags %}"
        '{% if project.project_type == "a4projects.Project" %}'
        "is a4 project"
        "{% else %}"
        "is no a4 project"
        "{% endif %}"
    )

    assert "is a4 project" == render_template(template, {"project": project})
    assert "is no a4 project" == render_template(
        template, {"project": external_project}
    )
    assert "is no a4 project" == render_template(template, {"project": bplan})
