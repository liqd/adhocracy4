import pytest

from adhocracy4.comments.models import Comment
from meinberlin.apps.exports import mixins


@pytest.mark.django_db
def test_reply_to_mixin(idea, comment_factory):
    mixin = mixins.ItemExportWithRepliesToMixin()

    virtual = mixin.get_virtual_fields({})
    assert 'replies_to' in virtual

    comment = comment_factory(content_object=idea)
    reply_comment = comment_factory(content_object=comment)

    assert Comment.objects.count() == 2

    assert mixin.get_replies_to_data(comment) == ''
    assert mixin.get_replies_to_data(reply_comment) == comment.id
