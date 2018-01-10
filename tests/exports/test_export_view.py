import pytest
from django.utils.translation import ugettext as _

from adhocracy4.ratings.models import Rating
from adhocracy4.exports.views import ItemExportView
from adhocracy4.exports.mixins import ItemExportWithRatesMixin
from adhocracy4.exports.mixins import ItemExportWithCommentCountMixin
from adhocracy4.exports.mixins import ItemExportWithCommentsMixin
from adhocracy4.exports.mixins import ItemExportWithLocationMixin
from tests.apps.ideas.models import Idea


@pytest.mark.django_db
def test_item_export(idea_factory, module, rf):
    request_ = rf.get('/')
    module_ = module

    class IdeaExportView(ItemExportView):
        model = Idea
        fields = ['name', 'creator', 'created']

        def get_queryset(self):
            return Idea.objects.order_by('id')

        request = request_
        module = module_

    idea0 = idea_factory(module=module)
    idea1 = idea_factory(module=module)

    view = IdeaExportView()

    header = [_('Link')] + [Idea._meta.get_field(name).verbose_name
                            for name in IdeaExportView.fields]
    assert view.get_header() == header

    rows = list(view.export_rows())
    assert len(rows) == 2

    assert rows[0][0].endswith(idea0.get_absolute_url())
    assert rows[0][1] == idea0.name
    assert rows[0][2] == idea0.creator.username
    assert rows[0][3] == idea0.created.isoformat()

    assert rows[1][0].endswith(idea1.get_absolute_url())
    assert rows[1][1] == idea1.name
    assert rows[1][2] == idea1.creator.username
    assert rows[1][3] == idea1.created.isoformat()


@pytest.mark.django_db
def test_item_text_cleanup(idea_factory, module, rf):
    request_ = rf.get('/')
    module_ = module

    class IdeaExportView(ItemExportView):
        model = Idea
        fields = ['description']

        def get_queryset(self):
            return Idea.objects.order_by('id')

        request = request_
        module = module_

    idea_factory(module=module, description='  <i>desc</i>ription ')

    view = IdeaExportView()
    rows = list(view.export_rows())
    assert rows[0][1] == 'description'


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
def test_item_location_mixin(idea):
    mixin = ItemExportWithLocationMixin()

    virtual = mixin.get_virtual_fields({})
    assert 'location' in virtual
    assert 'location_label' in virtual

    assert mixin.get_location_data({}) == ''
    assert mixin.get_location_label_data({}) == ''

    lon, lat = idea.point['geometry']['coordinates']
    assert mixin.get_location_data(idea) == '%s, %s' % (lon, lat)
    assert mixin.get_location_label_data(idea) == idea.point_label
