import pytest
import rules

from adhocracy4.test import helpers


@pytest.mark.django_db
def test_get_change_perm(rf, idea_factory):
    obj = idea_factory()
    request = rf.get("/")
    template = (
        "{% load item_tags %}"
        "{% get_item_view_permission obj as view_perm %}"
        "{% get_item_add_permission obj as add_perm %}"
        "{% get_item_change_permission obj as change_perm %}"
        "{% get_item_delete_permission obj as delete_perm %}"
        "{{ view_perm }}"
        "{{ add_perm }}"
        "{{ change_perm }}"
        "{{ delete_perm }}"
    )
    context = {"request": request, "obj": obj}
    helpers.render_template(template, context)

    assert "meinberlin_ideas.view_idea" == context["view_perm"]
    assert rules.perm_exists(context["view_perm"])
    assert "meinberlin_ideas.add_idea" == context["add_perm"]
    assert rules.perm_exists(context["add_perm"])
    assert "meinberlin_ideas.change_idea" == context["change_perm"]
    assert rules.perm_exists(context["change_perm"])
    assert "meinberlin_ideas.delete_idea" == context["delete_perm"]


@pytest.mark.django_db
def test_get_item_url(rf, idea_factory):
    obj = idea_factory()
    request = rf.get("/")
    template = (
        "{% load item_tags %}"
        "{% get_item_update_url obj as update_url %}"
        "{% get_item_delete_url obj as delete_url %}"
        "{{ update_url }}"
        "{{ delete_url }}"
    )
    context = {"request": request, "obj": obj}
    helpers.render_template(template, context)

    assert (
        "/ideas/{}-{}/update/".format(obj.created.year, "{:05d}".format(obj.pk))
        == context["update_url"]
    )
    assert (
        "/ideas/{}-{}/delete/".format(obj.created.year, "{:05d}".format(obj.pk))
        == context["delete_url"]
    )
