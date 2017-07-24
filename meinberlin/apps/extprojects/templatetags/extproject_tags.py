from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag
def extproject_url(project, viewname, *args, **kwargs):
    if hasattr(project, 'externalproject'):
        return project.externalproject.url

    if not args and not kwargs:
        kwargs['slug'] = project.slug
    return reverse(viewname, args=args, kwargs=kwargs)


@register.filter
def is_external(project):
    return hasattr(project, 'externalproject')
