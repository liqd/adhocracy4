import json

import pytest

from django.conf import settings
from django.views import generic as generic_views
from django.test.utils import override_settings

from adhocracy4.maps import mixins
from tests.apps.locations import models as location_models


@pytest.fixture
def location_detail_view():
    class FakeLocationDetailView(mixins.MapItemDetailMixin,
                                 generic_views.DetailView):
        model = location_models.Location
    return FakeLocationDetailView.as_view()


@pytest.fixture
def location_list_view(module):
    class FakeLocationListView(mixins.MapItemListMixin,
                               generic_views.ListView):
        model = location_models.Location

        def dispatch(self, *args, **kwargs):
            self.module = module
            return super().dispatch(*args, **kwargs)

    return FakeLocationListView.as_view()


@override_settings(BASE_MAP='https://{s}.tile.openstreetmap.org/')
@pytest.mark.django_db
def test_mapitem_detail_mixin(rf, location_detail_view, location, module,
                            area_settings):
    request = rf.get('/url')
    response = location_detail_view(request, pk=1)
    baseurl = response.context_data['baseurl']
    assert baseurl == settings.MAP_BASEURL


@override_settings(BASE_MAP='https://{s}.tile.openstreetmap.org/')
@pytest.mark.django_db
def test_mapitem_list_mixin(rf, location_list_view, location, module,
                            area_settings):
    request = rf.get('/url')
    response = location_list_view(request)
    baseurl = response.context_data['baseurl']
    mapitems_json = response.context_data['mapitems_json']
    polygon = json.loads(response.context_data['polygon'])
    assert baseurl == settings.MAP_BASEURL
    assert json.loads(mapitems_json) == {
        "type": "FeatureCollection",
        "features": [
            {
                "properties": {
                    "name": "",
                    "comments_count": "",
                    "url": "/location/1/",
                    "positive_rating_count": "",
                    "slug": "location",
                    "image": "",
                    "negative_rating_count": ""},
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [1.0, 1.0]
                }
            }
        ]
    }
    assert polygon == {
        'type': 'FeatureCollection',
        'features': [{
            'type': 'Feature',
            'properties': {},
            'geometry': {
                'type': 'Polygon',
                'coordinates': [
                    [[0.0, 0.0], [0.0, 1.0], [1.0, 1.0]]
                ]
            }
        }
        ]}
