from django import template

from meinberlin.apps.projects import get_project_type

register = template.Library()


@register.filter
def project_url(project):
    if get_project_type(project) in ('external', 'bplan'):
        return project.externalproject.url
    return project.get_absolute_url()


@register.filter
def project_type(project):
    return get_project_type(project)


@register.filter
def is_external(project):
    return get_project_type(project) in ('external', 'bplan')


@register.filter
def is_container(project):
    return get_project_type(project) == 'container'


@register.simple_tag
def to_class_name(value):
    return value.__class__.__name__
