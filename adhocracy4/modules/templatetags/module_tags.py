from django import template

register = template.Library()


@register.assignment_tag
def itemHasFeature(item, feature):
    return item.module.has_feature(feature, item.__class__)
