import json
from urllib.parse import unquote

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def closed_accordeons(context, project_id):
    request = context['request']
    cookie = request.COOKIES.get('dashboard_projects_closed_accordeons', '[]')
    ids = json.loads(unquote(cookie))
    if project_id in ids:
        ids.append(-1)
    return ids


@register.filter
def has_unpublishable_modules(project):
    """Check if modules can be removed from project.

    Modules can be removed if the project is not yet published and there is
    another module published for (added to) the project.
    """
    return (project.is_draft
            and project.published_modules.count() <= 1)
