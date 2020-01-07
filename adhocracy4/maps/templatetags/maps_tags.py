import json

from django import template
from django.conf import settings
from django.utils.html import format_html
from easy_thumbnails.files import get_thumbnailer

from adhocracy4.categories import get_category_pin_url

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
            category_icon = get_category_pin_url(item.category.icon)
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
def map_display_points(items, polygon, hideRatings='false'):
    use_vector_map = 0
    mapbox_token = ''
    omt_token = ''

    if (hasattr(settings, 'A4_USE_VECTORMAP') and
            settings.A4_USE_VECTORMAP):
        use_vector_map = 1

    if hasattr(settings, 'A4_MAPBOX_TOKEN'):
        mapbox_token = settings.A4_MAPBOX_TOKEN

    if hasattr(settings, 'A4_OPENMAPTILES_TOKEN'):
        omt_token = settings.A4_OPENMAPTILES_TOKEN

    return format_html(
        (
            '<div'
            ' style="height: 300px"'
            ' data-map="display_points"'
            ' data-baseurl="{baseurl}"'
            ' data-usevectormap="{usevectormap}"'
            ' data-mapbox-token="{mapbox_token}"'
            ' data-omt-token="{omt_token}"'
            ' data-attribution="{attribution}"'
            ' data-points="{points}"'
            ' data-polygon="{polygon}"'
            ' data-hide-ratings="{hideRatings}"'
            '></div>'
        ),
        baseurl=settings.A4_MAP_BASEURL,
        usevectormap=use_vector_map,
        mapbox_token=mapbox_token,
        omt_token=omt_token,
        attribution=settings.A4_MAP_ATTRIBUTION,
        points=get_points(items),
        polygon=json.dumps(polygon),
        hideRatings=hideRatings
    )


@register.simple_tag()
def map_display_point(point, polygon, pin_src=None):
    use_vector_map = 0
    mapbox_token = ''
    omt_token = ''

    if (hasattr(settings, 'A4_USE_VECTORMAP') and
            settings.A4_USE_VECTORMAP):
        use_vector_map = 1

    if hasattr(settings, 'A4_MAPBOX_TOKEN'):
        mapbox_token = settings.A4_MAPBOX_TOKEN

    if hasattr(settings, 'A4_OPENMAPTILES_TOKEN'):
        omt_token = settings.A4_OPENMAPTILES_TOKEN

    return format_html(
        (
            '<div'
            ' style="height: 300px"'
            ' data-map="display_point"'
            ' data-baseurl="{baseurl}"'
            ' data-usevectormap="{usevectormap}"'
            ' data-mapbox-token="{mapbox_token}"'
            ' data-omt-token="{omt_token}"'
            ' data-attribution="{attribution}"'
            ' data-point="{point}"'
            ' data-polygon="{polygon}"'
            ' data-pin-src="{pin_src}"'
            '></div>'
        ),
        baseurl=settings.A4_MAP_BASEURL,
        usevectormap=use_vector_map,
        mapbox_token=mapbox_token,
        omt_token=omt_token,
        attribution=settings.A4_MAP_ATTRIBUTION,
        point=json.dumps(point),
        polygon=json.dumps(polygon),
        pin_src=json.dumps(pin_src)
    )
