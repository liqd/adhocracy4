import factory
import pytest

from adhocracy4.test.helpers import render_template
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.budgeting import phases as budgeting_phases
from meinberlin.apps.ideas import phases as idea_phases
from meinberlin.apps.projects.templatetags.meinberlin_project_tags import (
    get_num_entries,
)
from tests.helpers import clear_query_cache


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


@pytest.mark.django_db
def test_get_num_entries(
    django_assert_num_queries,
    module_factory,
    phase_factory,
    idea_factory,
    proposal_factory,
    comment_factory,
):
    phase, module, project, idea = setup_phase(
        phase_factory, idea_factory, idea_phases.FeedbackPhase
    )
    phase1, module1, project1, proposal = setup_phase(
        phase_factory, proposal_factory, budgeting_phases.CollectPhase
    )
    empty_module = module_factory(project=project)

    # no items or comments
    clear_query_cache()
    with django_assert_num_queries(18):
        count = get_num_entries(empty_module)
        assert count == 0

    # one comment, no subcomments
    comment = comment_factory(content_object=idea)
    clear_query_cache()
    with django_assert_num_queries(18):
        count = get_num_entries(module)
        assert count == 2

    # two comments, no subcomments
    comment_1 = comment_factory(content_object=idea)
    clear_query_cache()
    with django_assert_num_queries(18):
        count = get_num_entries(module)
        assert count == 3

    # two subcomments for comment
    comment_factory(content_object=comment)
    comment_factory(content_object=comment)
    clear_query_cache()
    with django_assert_num_queries(18):
        count = get_num_entries(module)
        assert count == 5

    # two subcomments for comment_1
    comment_factory(content_object=comment_1)
    comment_factory(content_object=comment_1)
    clear_query_cache()
    with django_assert_num_queries(18):
        count = get_num_entries(module)
        assert count == 7

    # add another comment
    comment_factory(content_object=idea)
    clear_query_cache()
    with django_assert_num_queries(18):
        count = get_num_entries(module)
        assert count == 8

    # proposal comments
    proposal_comment = comment_factory(content_object=proposal)
    comment_factory(content_object=proposal_comment)
    comment_factory(content_object=proposal_comment)
    # add subcomments
    clear_query_cache()
    with django_assert_num_queries(18):
        count = get_num_entries(module1)
        assert count == 4
