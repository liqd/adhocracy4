import csv
from collections import OrderedDict

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FieldError
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.views import generic

from adhocracy4.comments.models import Comment
from adhocracy4.ratings.models import Rating


class VirtualFieldMixin:
    def get_virtual_fields(self):
        return OrderedDict()


class ItemExportView(generic.ListView, VirtualFieldMixin):
    fields = None
    exclude = None
    virtual = None
    model = None

    def __init__(self):
        super().__init__()
        if self.fields and self.exclude:
            raise FieldError()
        self._header, self._names = self._setup_fields()

    def _setup_fields(self):
        meta = self.model._meta
        exclude = self.exclude if self.exclude else []

        if self.fields:
            fields = [meta.get_field(name) for name in self.fields]
        else:
            fields = meta.get_fields()

        names = ['link']
        header = [_('Link')]
        for field in fields:
            if field.concrete \
                    and not (field.one_to_one and field.rel.parent_link) \
                    and field.attname not in exclude \
                    and field.attname not in names:

                names.append(field.attname)
                header.append(str(field.verbose_name))

        virtual = self.get_virtual_fields()
        for name, head in virtual.items():
            if name not in names:
                names.append(name)
                header.append(head)

        return header, names

    def get_queryset(self):
        return super().get_queryset()

    def get_virtual_fields(self):
        virtual = super().get_virtual_fields()
        if 'link' not in virtual:
            virtual['link'] = _('Link')
        return virtual

    def get_link_data(self, item):
        return self.request.build_absolute_uri(item.get_absolute_url())

    def get_field_data(self, item, name):
        # Use custom getters if they are defined
        get_field_attr_name = 'get_%s_data' % name
        if hasattr(self, get_field_attr_name):
            get_field_attr = getattr(self, get_field_attr_name)

            if hasattr(get_field_attr, '__call__'):
                return get_field_attr(item)
            return get_field_attr

        # If item is a dict, return the fields data by key
        try:
            if name in item:
                return item['name']
        except TypeError:
            pass

        # Finally try to get the fields data as a property
        return getattr(item, name, '')

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = (
            'attachment; filename="ideas.csv"'
        )

        writer = csv.writer(response, lineterminator='\n',
                            quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(self._header)

        for item in self.get_queryset().all():
            data = [self.get_field_data(item, name) for name in self._names]
            writer.writerow(data)

        return response


class ItemExportWithRatesMixin(VirtualFieldMixin):
    def get_virtual_fields(self):
        virtual = super().get_virtual_fields()
        if 'ratings_positive' not in virtual:
            virtual['ratings_positive'] = _('Positive ratings')
        if 'ratings_negative' not in virtual:
            virtual['ratings_negative'] = _('Negative ratings')

        return virtual

    def _count_ratings(self, item, value):
        ct = ContentType.objects.get_for_model(item)
        return Rating.objects.filter(content_type=ct, value=value).count()

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


class ItemExportWithCommentCountMixin(VirtualFieldMixin):
    def get_virtual_fields(self):
        virtual = super().get_virtual_fields()
        if 'comment_count' not in virtual:
            virtual['comment_count'] = _('Comment count')
        return virtual

    def get_comment_count_data(self, item):
        # FIXME: the annotated comment_count does currently not include replies
        # if hasattr(item, 'comment_count'):
        #     return item.comment_count
        if hasattr(item, 'comments'):
            return self._comment_count(item)

        return 0

    def _comment_count(self, item):
        comment_ids = item.comments.values_list('id', flat=True)
        replies = Comment.objects.filter(parent_comment__in=comment_ids)
        return len(comment_ids) + len(replies)


class ItemExportWithCommentsMixin(VirtualFieldMixin):
    COMMENT_FMT = '{date} - {username}\n{text}'
    REPLY_FMT = '@reply: {date} - {username}\n{text}'

    def get_virtual_fields(self):
        virtual = super().get_virtual_fields()
        if 'comments' not in virtual:
            virtual['comments'] = _('Comments')
        return virtual

    def get_comments_data(self, item):
        if hasattr(item, 'comments'):
            return '\n----\n'.join(self._flat_comments(item))
        return ''

    def _flat_comments(self, item):
        for comment in item.comments.all():
            yield self.COMMENT_FMT.format(
                date=comment.created.isoformat(),
                username=comment.creator.username,
                text=comment.comment.strip()
            )

            for reply in comment.child_comments.all():
                yield self.REPLY_FMT.format(
                    date=reply.created.isoformat(),
                    username=reply.creator.username,
                    text=reply.comment.strip()
                )
