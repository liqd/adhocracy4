import re

from django.utils.translation import gettext as _

from .base import VirtualFieldMixin


class CreatorContactExportMixin:
    """Add creator contact fields to exports."""

    def get_virtual_fields(self, virtual):
        virtual = super().get_virtual_fields(virtual)
        virtual["creator_contact_consent"] = str(_("Contact consent"))
        virtual["creator_email"] = str(_("Creator email"))
        virtual["creator_phone"] = str(_("Creator phone"))
        return virtual

    def get_field_data(self, item, name):
        """Handle contact fields."""
        if name == "creator_contact_consent":
            value = getattr(item, name, False)
            return "yes" if value else "no"

        if name in ["creator_email", "creator_phone"]:
            value = getattr(item, name, "")
            return str(value) if value else ""

        # Fall back to parent
        return super().get_field_data(item, name)


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


class ItemExportWithImageMixin(VirtualFieldMixin):
    """Adds image links to item export."""

    def get_virtual_fields(self, virtual):
        if "images" not in virtual:
            virtual["images"] = _("Images")
        return super().get_virtual_fields(virtual)

    def get_images(self, item):
        images = []

        if item.image:
            images.append(self.request.build_absolute_uri(item.image.url))

        description = str(getattr(item, "description", ""))
        if description:
            pattern = r'(?:src|href)="([^"]*?/uploads/[^"]*?)"'
            for url in re.findall(pattern, description):
                images.append(self.request.build_absolute_uri(url))

        return images

    def get_images_data(self, item):
        images = self.get_images(item)
        return images[0] if images else ""

    def get_extra_rows(self, item, names):
        images = self.get_images(item)
        if len(images) <= 1:
            return []

        images_index = names.index("images")
        reference_number_index = (
            names.index("reference_number") if "reference_number" in names else None
        )
        extra_rows = []
        for url in images[1:]:
            extra_row = [""] * len(names)
            extra_row[images_index] = url
            if reference_number_index is not None:
                extra_row[reference_number_index] = self.get_field_data(
                    item, "reference_number"
                )
            extra_rows.append(extra_row)
        return extra_rows
