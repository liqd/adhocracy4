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
