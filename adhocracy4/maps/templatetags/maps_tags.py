import json

from django import template
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import format_html
from easy_thumbnails.files import get_thumbnailer

register = template.Library()


def get_points(items):
    result = {}
    result['type'] = 'FeatureCollection'
    feature_list = []

    for item in items:

        image_url = ''
        comment_count = ''
        positive_rating_count = ''
        negative_rating_count = ''

        if hasattr(item, 'image') and item.image:
            image = get_thumbnailer(item.image)['map_thumbnail']
            image_url = image.url
        if hasattr(item, 'comment_count'):
            comment_count = item.comment_count
        if hasattr(item, 'positive_rating_count'):
            positive_rating_count = item.positive_rating_count
        if hasattr(item, 'negative_rating_count'):
            negative_rating_count = item.negative_rating_count

        if hasattr(item, 'category') and getattr(item.category, 'icon', None):
            category_icon = static('category_icons/pins/{}_pin.svg'.
                                   format(item.category.icon))
        else:
            category_icon = ''

        properties = {
            'name': item.name,
            'slug': item.slug,
            'image': image_url,
            'comments_count': comment_count,
            'positive_rating_count': positive_rating_count,
            'negative_rating_count': negative_rating_count,
            'url': item.get_absolute_url(),
            'category_icon': category_icon
        }
        point_dict = item.point
        point_dict['properties'] = properties
        feature_list.append(point_dict)

    result['features'] = feature_list
    return json.dumps(result)


@register.simple_tag()
def map_display_points(items, polygon):
    return format_html(
        (
            '<div'
            ' style="height: 300px"'
            ' data-map="display_points"'
            ' data-baseurl="{baseurl}"'
            ' data-attribution="{attribution}"'
            ' data-points="{points}"'
            ' data-polygon="{polygon}"'
            '></div>'
        ),
        baseurl=settings.A4_MAP_BASEURL,
        attribution=settings.A4_MAP_ATTRIBUTION,
        points=get_points(items),
        polygon=json.dumps(polygon)
    )


@register.simple_tag()
def map_display_point(point, polygon, category_icon=None):
    return format_html(
        (
            '<div'
            ' style="height: 300px"'
            ' data-map="display_point"'
            ' data-baseurl="{baseurl}"'
            ' data-attribution="{attribution}"'
            ' data-point="{point}"'
            ' data-polygon="{polygon}"'
            ' data-category-icon="{category_icon}"'
            '></div>'
        ),
        baseurl=settings.A4_MAP_BASEURL,
        attribution=settings.A4_MAP_ATTRIBUTION,
        point=json.dumps(point),
        polygon=json.dumps(polygon),
        category_icon=json.dumps(category_icon)
    )
