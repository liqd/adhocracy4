from django.conf import settings
from easy_thumbnails.files import get_thumbnailer


class MapItemListMixin(object):

    def dump_geojson(self):
        result = {}
        result['type'] = 'FeatureCollection'
        feature_list = []

        for item in super().get_queryset():

            url = ''

            if hasattr(item, 'image') and item.image:
                image = get_thumbnailer(item.image)['map_thumbnail']
                url = image.url

            properties = {
                'name': item.name,
                'slug': item.slug,
                'image':  url,
                'comments_count': item.comment_count,
                'positive_rating_count': item.positive_rating_count,
                'negative_rating_count': item.negative_rating_count,
                'url': item.get_absolute_url()
            }
            point_dict = item.point
            point_dict['properties'] = properties
            feature_list.append(point_dict)

        result['features'] = feature_list
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mapideas_json'] = self.dump_geojson()
        context['map_url'] = settings.BASE_MAP
        context['polygon'] = self.module.settings_instance.polygon
        return context


class MapItemDetailMixin(object):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['map_url'] = settings.BASE_MAP
        return context
