import pytest

from adhocracy4.exports.mixins import ItemExportWithRatesMixin
from adhocracy4.ratings.models import Rating
from tests.apps.ideas.models import Idea


@pytest.mark.django_db
def test_item_rates_mixin(idea, rating_factory):
    rating_factory(content_object=idea, value=Rating.POSITIVE)
    rating_factory(content_object=idea, value=Rating.NEGATIVE)

    mixin = ItemExportWithRatesMixin()

    virtual = mixin.get_virtual_fields({})
    assert "ratings_positive" in virtual
    assert "ratings_negative" in virtual

    # Test explicit count
    assert mixin.get_ratings_positive_data({}) == 0
    assert mixin.get_ratings_positive_data(idea) == 1
    assert mixin.get_ratings_negative_data({}) == 0
    assert mixin.get_ratings_negative_data(idea) == 1

    # Test annotated counting
    idea = (
        Idea.objects.annotate_positive_rating_count()
        .annotate_negative_rating_count()
        .first()
    )
    assert mixin.get_ratings_positive_data(idea) == 1
    assert mixin.get_ratings_negative_data(idea) == 1
