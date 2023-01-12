import pytest

from adhocracy4.exports.mixins import ItemExportWithLinkMixin
from adhocracy4.exports.mixins import ItemExportWithLocationMixin
from adhocracy4.exports.mixins import UserGeneratedContentExportMixin


@pytest.mark.django_db
def test_user_generated_content_mixin(idea):
    mixin = UserGeneratedContentExportMixin()

    virtual = mixin.get_virtual_fields({})
    assert "creator" in virtual
    assert "created" in virtual

    assert idea.creator.username == mixin.get_creator_data(idea)
    assert idea.created.astimezone().isoformat() == mixin.get_created_data(idea)


@pytest.mark.django_db
def test_item_link_mixin(rf, idea):
    request = rf.get("/")
    mixin = ItemExportWithLinkMixin()
    mixin.request = request

    virtual = mixin.get_virtual_fields({})
    assert "link" in virtual

    absolute_url = idea.get_absolute_url()
    assert mixin.get_link_data(idea) == "http://testserver" + absolute_url


@pytest.mark.django_db
def test_item_location_mixin(idea):
    mixin = ItemExportWithLocationMixin()

    virtual = mixin.get_virtual_fields({})
    assert "location_lon" in virtual
    assert "location_lat" in virtual
    assert "location_label" in virtual

    assert mixin.get_location_lon_data({}) == ""
    assert mixin.get_location_lat_data({}) == ""
    assert mixin.get_location_label_data({}) == ""

    lon, lat = idea.point["geometry"]["coordinates"]
    assert mixin.get_location_lon_data(idea) == lon
    assert mixin.get_location_lat_data(idea) == lat
    assert mixin.get_location_label_data(idea) == idea.point_label
