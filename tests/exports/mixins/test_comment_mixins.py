import pytest

from adhocracy4.comments.models import Comment
from adhocracy4.exports.mixins import CommentExportWithRepliesToMixin
from adhocracy4.exports.mixins import CommentExportWithRepliesToReferenceMixin
from adhocracy4.exports.mixins import ItemExportWithCommentCountMixin
from adhocracy4.exports.mixins import ItemExportWithCommentsMixin
from tests.apps.ideas.models import Idea


@pytest.mark.django_db
def test_item_comment_count_mixin(idea, comment_factory):
    comment_factory(content_object=idea)
    comment = comment_factory(content_object=idea)
    comment_factory(content_object=comment)

    mixin = ItemExportWithCommentCountMixin()

    virtual = mixin.get_virtual_fields({})
    assert "comment_count" in virtual

    # Test explicit count
    assert mixin.get_comment_count_data({}) == 0
    assert mixin.get_comment_count_data(idea) == 3

    # Test annotated counting
    idea = Idea.objects.annotate_comment_count().first()
    assert mixin.get_comment_count_data(idea) == 3


@pytest.mark.django_db
def test_item_comments_mixin(idea, comment_factory):
    comment = comment_factory(comment="comment", content_object=idea)
    comment_factory(comment="reply to comment", content_object=comment)
    comment_factory(comment="<i>comment</i>2   ", content_object=idea)

    mixin = ItemExportWithCommentsMixin()

    virtual = mixin.get_virtual_fields({})
    assert "comments" in virtual

    assert mixin.get_comments_data({}) == ""
    data = mixin.get_comments_data(idea)
    assert "comment" in data
    assert "reply to comment" in data
    assert "comment2" in data
    assert "<i>comment</i>" not in data
    assert "2   " not in data


@pytest.mark.django_db
def test_reply_to_mixin(idea, comment_factory):
    mixin = CommentExportWithRepliesToMixin()

    virtual = mixin.get_virtual_fields({})
    assert "replies_to_comment" in virtual

    comment = comment_factory(content_object=idea)
    reply_comment = comment_factory(content_object=comment)

    assert Comment.objects.count() == 2

    assert mixin.get_replies_to_comment_data(comment) == ""
    assert mixin.get_replies_to_comment_data(reply_comment) == comment.id


@pytest.mark.django_db
def test_reply_to_reference_mixin(idea, comment_factory):
    mixin = CommentExportWithRepliesToReferenceMixin()

    virtual = mixin.get_virtual_fields({})
    assert "replies_to_reference" in virtual

    comment = comment_factory(content_object=idea)
    reply_comment = comment_factory(content_object=comment)

    assert Comment.objects.count() == 2

    assert mixin.get_replies_to_reference_data(comment) == idea.reference_number
    assert mixin.get_replies_to_reference_data(reply_comment) == ""
