from django import template

from adhocracy4.categories import get_category_pin_url

register = template.Library()


@register.simple_tag(name='get_category_pin_url')
def get_category_pin_url_tag(item):
    if hasattr(item, 'category'):
        icon_name = getattr(item.category, 'icon', None)
        return get_category_pin_url(icon_name)
