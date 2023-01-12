from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _

from adhocracy4.ratings.models import Rating

from .base import VirtualFieldMixin


class ItemExportWithRatesMixin(VirtualFieldMixin):
    """
    Adds positive and negative ratings count to an item.
    """

    def get_virtual_fields(self, virtual):
        if "ratings_positive" not in virtual:
            virtual["ratings_positive"] = _("Positive ratings")
        if "ratings_negative" not in virtual:
            virtual["ratings_negative"] = _("Negative ratings")

        return super().get_virtual_fields(virtual)

    def get_ratings_positive_data(self, item):
        if hasattr(item, "positive_rating_count"):
            return item.positive_rating_count

        if hasattr(item, "ratings"):
            return self._count_ratings(item, Rating.POSITIVE)

        return 0

    def get_ratings_negative_data(self, item):
        if hasattr(item, "negative_rating_count"):
            return item.negative_rating_count

        if hasattr(item, "ratings"):
            return self._count_ratings(item, Rating.NEGATIVE)

        return 0

    def _count_ratings(self, item, value):
        ct = ContentType.objects.get_for_model(item)
        return Rating.objects.filter(
            content_type=ct, object_pk=item.pk, value=value
        ).count()
