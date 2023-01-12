from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext as _

from adhocracy4.comments.models import Comment
from adhocracy4.exports import unescape_and_strip_html

from .base import VirtualFieldMixin


class ItemExportWithCommentCountMixin(VirtualFieldMixin):
    """
    Adds the comment count (including child comments) to an item.
    """

    def get_virtual_fields(self, virtual):
        if "comment_count" not in virtual:
            virtual["comment_count"] = _("Comment count")
        return super().get_virtual_fields(virtual)

    def get_comment_count_data(self, item):
        # FIXME: the annotated comment_count does currently not include replies
        # if hasattr(item, 'comment_count'):
        #     return item.comment_count
        if hasattr(item, "comments"):
            return self._count_comments(item)

        return 0

    def _count_comments(self, item):
        comment_ids = item.comments.values_list("id", flat=True)
        replies = Comment.objects.filter(parent_comment__in=comment_ids)
        return len(comment_ids) + len(replies)


class ItemExportWithCommentsMixin(VirtualFieldMixin):
    """
    Adds the comments to the item.

    This is meant to be used in an item (not comment) export. It adds
    all comments and the replies to the same line as the item.
    """

    COMMENT_FMT = "{date} - {username}\n{text}"
    REPLY_FMT = "@reply: {date} - {username}\n{text}"

    def get_virtual_fields(self, virtual):
        if "comments" not in virtual:
            virtual["comments"] = _("Comments")
        return super().get_virtual_fields(virtual)

    def get_comments_data(self, item):
        if hasattr(item, "comments"):
            return "\n----\n".join(self._flat_comments(item))
        return ""

    def _flat_comments(self, item):
        for comment in item.comments.all():
            yield self.COMMENT_FMT.format(
                date=comment.created.astimezone().isoformat(),
                username=comment.creator.username,
                text=unescape_and_strip_html(comment.comment),
            )

            for reply in comment.child_comments.all():
                yield self.REPLY_FMT.format(
                    date=reply.created.astimezone().isoformat(),
                    username=reply.creator.username,
                    text=unescape_and_strip_html(reply.comment),
                )


class CommentExportWithRepliesToMixin(VirtualFieldMixin):
    """
    Adds the id of a comment the comment is a reply to.

    To be used in comment exports.
    """

    def get_virtual_fields(self, virtual):
        virtual["replies_to_comment"] = _("Reply to Comment")
        return super().get_virtual_fields(virtual)

    def get_replies_to_comment_data(self, comment):
        try:
            return comment.parent_comment.get().pk
        except ObjectDoesNotExist:
            return ""


class CommentExportWithRepliesToReferenceMixin(VirtualFieldMixin):
    """
    Adds the reference number of an item the comment is a reply to.

    To be used in comment exports. Only to be used with items that have a
    reference number.
    """

    def get_virtual_fields(self, virtual):
        virtual["replies_to_reference"] = _("Reply to Reference")
        return super().get_virtual_fields(virtual)

    def get_replies_to_reference_data(self, comment):
        if hasattr(comment.content_object, "reference_number"):
            return comment.content_object.reference_number
        else:
            return ""
