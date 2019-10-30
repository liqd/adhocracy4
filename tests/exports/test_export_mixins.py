from collections import OrderedDict

import pytest

from adhocracy4.exports.mixins import ExportModelFieldsMixin
from adhocracy4.exports.mixins import ItemExportWithCategoriesMixin
from adhocracy4.exports.mixins import ItemExportWithCommentCountMixin
from adhocracy4.exports.mixins import ItemExportWithCommentsMixin
from adhocracy4.exports.mixins import ItemExportWithLinkMixin
from adhocracy4.exports.mixins import ItemExportWithLocationMixin
from adhocracy4.exports.mixins import ItemExportWithRatesMixin
from adhocracy4.ratings.models import Rating
from tests.apps.ideas.models import Idea


@pytest.mark.django_db
def test_item_link_mixin(rf, idea):
    request = rf.get('/')
    mixin = ItemExportWithLinkMixin()
    mixin.request = request

    virtual = mixin.get_virtual_fields({})
    assert 'link' in virtual

    absolute_url = idea.get_absolute_url()
    assert mixin.get_link_data(idea) == 'http://testserver' + absolute_url


@pytest.mark.django_db
def test_model_fields_mixin(idea):
    class Mixin(ExportModelFieldsMixin):
        model = Idea
        fields = ['description', 'name']
        html_fields = ['description']

    mixin = Mixin()

    virtual = mixin.get_virtual_fields(OrderedDict())
    assert list(virtual.items()) == [
        ('description', 'Description'),
        ('name', 'name')
    ]

    idea.description = '&nbsp; &amp;&euro;&lt;&quot;&auml;&ouml;&uuml;' \
                       '&#x1F4A9;&nbsp; '
    assert mixin.get_description_data(idea) == '&€<"äöü💩'


@pytest.mark.django_db
def test_model_fields_mixin_exclude(idea):
    class Mixin(ExportModelFieldsMixin):
        model = Idea
        exclude = ['point', 'point_label']

    mixin = Mixin()

    virtual = mixin.get_virtual_fields({})

    assert sorted(virtual.keys()) == ['category', 'created', 'creator',
                                      'description', 'id', 'modified',
                                      'module', 'name']


@pytest.mark.django_db
def test_item_rates_mixin(idea, rating_factory):
    rating_factory(content_object=idea, value=Rating.POSITIVE)
    rating_factory(content_object=idea, value=Rating.NEGATIVE)

    mixin = ItemExportWithRatesMixin()

    virtual = mixin.get_virtual_fields({})
    assert 'ratings_positive' in virtual
    assert 'ratings_negative' in virtual

    # Test explicit count
    assert mixin.get_ratings_positive_data({}) == 0
    assert mixin.get_ratings_positive_data(idea) == 1
    assert mixin.get_ratings_negative_data({}) == 0
    assert mixin.get_ratings_negative_data(idea) == 1

    # Test annotated counting
    idea = Idea.objects \
        .annotate_positive_rating_count() \
        .annotate_negative_rating_count() \
        .first()
    assert mixin.get_ratings_positive_data(idea) == 1
    assert mixin.get_ratings_negative_data(idea) == 1


@pytest.mark.django_db
def test_item_comment_count_mixin(idea, comment_factory):
    comment_factory(content_object=idea)
    comment = comment_factory(content_object=idea)
    comment_factory(content_object=comment)

    mixin = ItemExportWithCommentCountMixin()

    virtual = mixin.get_virtual_fields({})
    assert 'comment_count' in virtual

    # Test explicit count
    assert mixin.get_comment_count_data({}) == 0
    assert mixin.get_comment_count_data(idea) == 3

    # Test annotated counting
    idea = Idea.objects \
        .annotate_comment_count() \
        .first()
    assert mixin.get_comment_count_data(idea) == 3


@pytest.mark.django_db
def test_item_comments_mixin(idea, comment_factory):
    comment = comment_factory(comment='comment', content_object=idea)
    comment_factory(comment='reply to comment', content_object=comment)
    comment_factory(comment='<i>comment</i>2   ', content_object=idea)

    mixin = ItemExportWithCommentsMixin()

    virtual = mixin.get_virtual_fields({})
    assert 'comments' in virtual

    assert mixin.get_comments_data({}) == ''
    data = mixin.get_comments_data(idea)
    assert 'comment' in data
    assert 'reply to comment' in data
    assert 'comment2' in data
    assert '<i>comment</i>' not in data
    assert '2   ' not in data


@pytest.mark.django_db
def test_item_categories_mixin(idea, category):

    idea.category = category
    idea.save()

    mixin = ItemExportWithCategoriesMixin()

    virtual = mixin.get_virtual_fields({})
    assert 'category' in virtual

    data = mixin.get_category_data(idea)

    assert category.name in data


@pytest.mark.django_db
def test_item_location_mixin(idea):
    mixin = ItemExportWithLocationMixin()

    virtual = mixin.get_virtual_fields({})
    assert 'location_lon' in virtual
    assert 'location_lat' in virtual
    assert 'location_label' in virtual

    assert mixin.get_location_lon_data({}) == ''
    assert mixin.get_location_lat_data({}) == ''
    assert mixin.get_location_label_data({}) == ''

    lon, lat = idea.point['geometry']['coordinates']
    assert mixin.get_location_lon_data(idea) == lon
    assert mixin.get_location_lat_data(idea) == lat
    assert mixin.get_location_label_data(idea) == idea.point_label
