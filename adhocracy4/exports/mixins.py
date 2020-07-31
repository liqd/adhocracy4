from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _

from adhocracy4.comments.models import Comment
from adhocracy4.ratings.models import Rating

from . import unescape_and_strip_html


class VirtualFieldMixin:
    def get_virtual_fields(self, virtual):
        return virtual


class ItemExportWithLinkMixin(VirtualFieldMixin):
    def get_virtual_fields(self, virtual):
        if 'link' not in virtual:
            virtual['link'] = _('Link')
        return super().get_virtual_fields(virtual)

    def get_link_data(self, item):
        return self.request.build_absolute_uri(item.get_absolute_url())


class ExportModelFieldsMixin(VirtualFieldMixin):
    # Requires self.model to be set
    fields = None
    exclude = None
    html_fields = None

    def get_virtual_fields(self, virtual):
        meta = self.model._meta
        exclude = self.exclude if self.exclude else []

        if self.fields:
            fields = [meta.get_field(name) for name in self.fields]
        else:
            fields = meta.get_fields()

        for field in fields:
            if field.concrete \
                    and not (field.one_to_one
                             and field.remote_field.parent_link) \
                    and field.name not in exclude \
                    and field.name not in virtual:
                virtual[field.name] = str(field.verbose_name)

        self._setup_html_fields()

        return super().get_virtual_fields(virtual)

    def _setup_html_fields(self):
        html_fields = self.html_fields if self.html_fields else []
        for field in html_fields:
            get_field_attr_name = 'get_%s_data' % field
            setattr(self, get_field_attr_name,
                    lambda item, field_name=field:
                    unescape_and_strip_html(getattr(item, field_name)))


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
                text=unescape_and_strip_html(comment.comment)
            )

            for reply in comment.child_comments.all():
                yield self.REPLY_FMT.format(
                    date=reply.created.isoformat(),
                    username=reply.creator.username,
                    text=unescape_and_strip_html(reply.comment)
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


class ItemExportWithLabelsMixin(VirtualFieldMixin):

    def get_virtual_fields(self, virtual):
        if 'labels' not in virtual:
            virtual['labels'] = _('Labels')
        return super().get_virtual_fields(virtual)

    def get_labels_data(self, item):
        if hasattr(item, 'labels') and item.labels:
            return ', '.join(item.labels.all().values_list('name', flat=True))
        return ''


class ItemExportWithLocationMixin(VirtualFieldMixin):
    def get_virtual_fields(self, virtual):
        if 'location_lon' not in virtual:
            virtual['location_lon'] = _('Location (Longitude)')
        if 'location_lat' not in virtual:
            virtual['location_lat'] = _('Location (Latitude)')
        if 'location_label' not in virtual:
            virtual['location_label'] = _('Location label')
        return super().get_virtual_fields(virtual)

    def get_location_lon_data(self, item):
        if hasattr(item, 'point'):
            point = item.point
            try:
                if 'geometry' in point:
                    return point['geometry']['coordinates'][0]
            except TypeError:
                pass
        return ''

    def get_location_lat_data(self, item):
        if hasattr(item, 'point'):
            point = item.point
            try:
                if 'geometry' in point:
                    return point['geometry']['coordinates'][1]
            except TypeError:
                pass
        return ''

    def get_location_label_data(self, item):
        return getattr(item, 'point_label', '')
