import pytest
import rules

from adhocracy4.test import helpers


@pytest.mark.django_db
def test_get_change_perm(rf, map_idea_factory):
    obj = map_idea_factory()
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

    assert "meinberlin_mapideas.view_mapidea" == context["view_perm"]
    assert rules.perm_exists(context["view_perm"])
    assert "meinberlin_mapideas.add_mapidea" == context["add_perm"]
    assert rules.perm_exists(context["add_perm"])
    assert "meinberlin_mapideas.change_mapidea" == context["change_perm"]
    assert rules.perm_exists(context["change_perm"])
    assert "meinberlin_mapideas.delete_mapidea" == context["delete_perm"]
