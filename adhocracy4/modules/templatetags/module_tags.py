from django import template

register = template.Library()


@register.filter
def has_feature(item, feature):
    return item.module.has_feature(feature, item.__class__)
