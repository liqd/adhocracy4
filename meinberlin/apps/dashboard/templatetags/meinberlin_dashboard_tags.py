import json
from urllib.parse import unquote

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def closed_accordions(context, project_id):
    request = context["request"]
    cookie = request.COOKIES.get("dashboard_projects_closed_accordions", "[]")
    ids = json.loads(unquote(cookie))
    if project_id in ids:
        ids.append(-1)
    return ids


@register.filter
def is_publishable(project, project_progress):
    """Check if project can be published.

    Required project details need to be filled in and at least one module
    has to be published (added to the project).
    """
    return (
        project_progress["project_is_complete"]
        and project.published_modules.count() >= 1
    )


@register.filter
def has_unpublishable_modules(project):
    """Check if modules can be removed from project.

    Modules can be removed if the project is not yet published and there is
    another module published for (added to) the project.
    """
    return project.is_draft and project.published_modules.count() > 1


@register.filter
def project_nav_is_active(dashboard_menu_project):
    """Check if the view is in the project dashboard nav."""
    for item in dashboard_menu_project:
        if item["is_active"]:
            return True
    return False


@register.filter
def module_nav_is_active(dashboard_menu_modules):
    """Check if the view is in the project dashboard nav."""
    for module_menu in dashboard_menu_modules:
        for item in module_menu["menu"]:
            if item["is_active"]:
                return True
    return False


@register.filter
def has_publishable_module(dashboard_menu_modules):
    for module_menu in dashboard_menu_modules:
        if module_menu["is_complete"]:
            return True
    return False
