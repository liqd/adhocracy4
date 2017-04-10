import json

from django.conf import settings
from easy_thumbnails.files import get_thumbnailer


class MapItemListMixin(object):

    def dump_geojson(self):
        result = {}
        result['type'] = 'FeatureCollection'
        feature_list = []

        for item in super().get_queryset():

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

            properties = {
                'name': item.name,
                'slug': item.slug,
                'image':  image_url,
                'comments_count': comment_count,
                'positive_rating_count': positive_rating_count,
                'negative_rating_count': negative_rating_count,
                'url': item.get_absolute_url()
            }
            point_dict = item.point
            point_dict['properties'] = properties
            feature_list.append(point_dict)

        result['features'] = feature_list
        return json.dumps(result)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mapitems_json'] = self.dump_geojson()
        context['baseurl'] = settings.MAP_BASEURL
        context['polygon'] = json.dumps(self.module.settings_instance.polygon)
        return context


class MapItemDetailMixin(object):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['baseurl'] = settings.MAP_BASEURL
        context['polygon'] = json.dumps(self.object.module.settings_instance
                                        .polygon)
        context['point'] = json.dumps(self.object.point)
        return context
