from django import template

from .. import utils

register = template.Library()


@register.simple_tag
def get_moderated_projects(user):
    return utils.get_moderated_projects(user)


@register.simple_tag
def user_moderates_any_project(user):
    return utils.user_moderates_any_project(user)


@register.simple_tag(takes_context=True)
def moderation_page_url(context, page):
    request = context["request"]
    params = request.GET.copy()
    params["page"] = page
    return "?{}".format(params.urlencode())
