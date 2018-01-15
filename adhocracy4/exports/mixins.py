from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _

from adhocracy4.comments.models import Comment
from adhocracy4.ratings.models import Rating


class VirtualFieldMixin:
    def get_virtual_fields(self, virtual):
        return virtual


class ItemExportWithRatesMixin(VirtualFieldMixin):
    def get_virtual_fields(self, virtual):
        if 'ratings_positive' not in virtual:
            virtual['ratings_positive'] = _('Positive ratings')
        if 'ratings_negative' not in virtual:
            virtual['ratings_negative'] = _('Negative ratings')

        return super().get_virtual_fields(virtual)

    def get_ratings_positive_data(self, item):
        if hasattr(item, 'positive_rating_count'):
            return item.positive_rating_count

        if hasattr(item, 'ratings'):
            return self._count_ratings(item, Rating.POSITIVE)

        return 0

    def get_ratings_negative_data(self, item):
        if hasattr(item, 'negative_rating_count'):
            return item.negative_rating_count

        if hasattr(item, 'ratings'):
            return self._count_ratings(item, Rating.NEGATIVE)

        return 0

    def _count_ratings(self, item, value):
        ct = ContentType.objects.get_for_model(item)
        return Rating.objects.filter(
            content_type=ct,
            object_pk=item.pk,
            value=value).count()


class ItemExportWithCommentCountMixin(VirtualFieldMixin):
    def get_virtual_fields(self, virtual):
        if 'comment_count' not in virtual:
            virtual['comment_count'] = _('Comment count')
        return super().get_virtual_fields(virtual)

    def get_comment_count_data(self, item):
        # FIXME: the annotated comment_count does currently not include replies
        # if hasattr(item, 'comment_count'):
        #     return item.comment_count
        if hasattr(item, 'comments'):
            return self._count_comments(item)

        return 0

    def _count_comments(self, item):
        comment_ids = item.comments.values_list('id', flat=True)
        replies = Comment.objects.filter(parent_comment__in=comment_ids)
        return len(comment_ids) + len(replies)


class ItemExportWithCommentsMixin(VirtualFieldMixin):
    COMMENT_FMT = '{date} - {username}\n{text}'
    REPLY_FMT = '@reply: {date} - {username}\n{text}'

    def get_virtual_fields(self, virtual):
        if 'comments' not in virtual:
            virtual['comments'] = _('Comments')
        return super().get_virtual_fields(virtual)

    def get_comments_data(self, item):
        if hasattr(item, 'comments'):
            return '\n----\n'.join(self._flat_comments(item))
        return ''

    def _flat_comments(self, item):
        for comment in item.comments.all():
            yield self.COMMENT_FMT.format(
                date=comment.created.isoformat(),
                username=comment.creator.username,
                text=self.strip_and_unescape_html(comment.comment)
            )

            for reply in comment.child_comments.all():
                yield self.REPLY_FMT.format(
                    date=reply.created.isoformat(),
                    username=reply.creator.username,
                    text=self.strip_and_unescape_html(reply.comment).strip()
                )


class ItemExportWithCategoriesMixin(VirtualFieldMixin):

    def get_virtual_fields(self, virtual):
        if 'category' not in virtual:
            virtual['category'] = _('Category')
        return super().get_virtual_fields(virtual)

    def get_category_data(self, item):
        if hasattr(item, 'category') and item.category:
            return item.category.name
        return ''


class ItemExportWithLocationMixin(VirtualFieldMixin):
    def get_virtual_fields(self, virtual):
        if 'location' not in virtual:
            virtual['location'] = _('Location')
        if 'location_label' not in virtual:
            virtual['location_label'] = _('Location label')
        return super().get_virtual_fields(virtual)

    def get_location_data(self, item):
        if hasattr(item, 'point'):
            point = item.point
            if 'geometry' in point:
                return ', '.join(map(str, point['geometry']['coordinates']))
        return ''

    def get_location_label_data(self, item):
        return getattr(item, 'point_label', '')
