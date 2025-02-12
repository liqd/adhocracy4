from django.utils.translation import gettext as _

from .base import VirtualFieldMixin


class UserGeneratedContentExportMixin(VirtualFieldMixin):
    """
    Adds link to item.

    Can be used with all suitable models, not only module items.
    """

    def get_virtual_fields(self, virtual):
        if "creator" not in virtual:
            virtual["creator"] = _("Creator")
        if "created" not in virtual:
            virtual["created"] = _("Created")
        return super().get_virtual_fields(virtual)

    def get_creator_data(self, item):
        return item.creator.username

    def get_created_data(self, item):
        return item.created.astimezone().isoformat()


class ItemExportWithLinkMixin(VirtualFieldMixin):
    """
    Adds link to item.

    Can be used with all suitable models, not only module items.
    """

    def get_virtual_fields(self, virtual):
        if "link" not in virtual:
            virtual["link"] = _("Link")
        return super().get_virtual_fields(virtual)

    def get_link_data(self, item):
        return self.request.build_absolute_uri(item.get_absolute_url())


class ItemExportWithLocationMixin(VirtualFieldMixin):
    """
    Adds location (LON, LAT, and label) to item.

    Can be used with all suitable models, not only module items.
    """

    def get_virtual_fields(self, virtual):
        if "location_lon" not in virtual:
            virtual["location_lon"] = _("Location (Longitude)")
        if "location_lat" not in virtual:
            virtual["location_lat"] = _("Location (Latitude)")
        if "location_label" not in virtual:
            virtual["location_label"] = _("Location label")
        return super().get_virtual_fields(virtual)

    def get_location_lon_data(self, item):
        if hasattr(item, "point"):
            point = item.point
            if hasattr(point, "geojson"):
                return point.x
            try:
                if "geometry" in point:
                    return point["geometry"]["coordinates"][0]
            except TypeError:
                pass
        return ""

    def get_location_lat_data(self, item):
        if hasattr(item, "point"):
            point = item.point
            if hasattr(point, "geojson"):
                return point.y
            try:
                if "geometry" in point:
                    return point["geometry"]["coordinates"][1]
            except TypeError:
                pass
        return ""

    def get_location_label_data(self, item):
        return getattr(item, "point_label", "")
