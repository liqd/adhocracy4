import csv
from collections import OrderedDict

import xlsxwriter
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FieldError
from django.http import HttpResponse
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.translation import ugettext as _
from django.views import generic

from adhocracy4.comments.models import Comment
from adhocracy4.modules import models as module_models
from adhocracy4.projects.mixins import ProjectMixin
from adhocracy4.ratings.models import Rating
from adhocracy4.rules import mixins as rules_mixins

from . import exports


class ExportModuleDispatcher(rules_mixins.PermissionRequiredMixin,
                             generic.View):
    permission_required = 'a4projects.change_project'

    def dispatch(self, request, *args, **kwargs):
        export_id = int(kwargs.pop('export_id'))
        module = module_models.Module.objects.get(slug=kwargs['module_slug'])
        project = module.project

        self.project = project

        # Since the PermissionRequiredMixin.dispatch method is never called
        # we have to check permissions manually
        if not self.has_permission():
            return self.handle_no_permission()

        module_exports = exports[module]
        assert len(module_exports) > export_id

        # Dispatch the request to the export view
        view = module_exports[export_id][1].as_view()
        return view(request, module=module, *args, **kwargs)

    def get_permission_object(self):
        return self.project


class AbstractCSVExportView(generic.View):
    def get_filename(self):
        return '%s.csv' % (self.get_base_filename())

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = \
            'attachment; filename="%s"' % self.get_filename()

        writer = csv.writer(response, lineterminator='\n',
                            quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(self.get_header())
        writer.writerows(self.export_rows())

        return response


class AbstractXlsxExportView(generic.View):

    def get_filename(self):
        return '%s.xlsx' % (self.get_base_filename())

    def get(self, request, *args, **kwargs):
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument'
                         '.spreadsheetml.sheet')
        response['Content-Disposition'] = \
            'attachment; filename="%s"' % self.get_filename()

        workbook = xlsxwriter.Workbook(response, {
            'in_memory': True,
            'strings_to_formulas': False
        })
        worksheet = workbook.add_worksheet()

        for colnum, field in enumerate(self.get_header()):
            worksheet.write(0, colnum, field)

        for rownum, row in enumerate(self.export_rows(), start=1):
            for colnum, field in enumerate(row):
                worksheet.write(rownum, colnum, self._clean_field(field))

        workbook.close()

        return response

    def _clean_field(self, field):
        if isinstance(field, str):
            return field.replace('\r', '')
        return field


class VirtualFieldMixin:
    def get_virtual_fields(self, virtual):
        return virtual


class ItemExportView(ProjectMixin,
                     VirtualFieldMixin,
                     generic.list.MultipleObjectMixin,
                     AbstractXlsxExportView,):
    fields = None
    exclude = None
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

        # Ensure that link is the first row even though it's a virtual field
        names = ['link']
        header = [_('Link')]

        for field in fields:
            if field.concrete \
                    and not (field.one_to_one and field.rel.parent_link) \
                    and field.name not in exclude \
                    and field.name not in names:
                names.append(field.name)
                header.append(str(field.verbose_name))

        # Get virtual fields in their order from the Mixins
        virtual = OrderedDict()
        virtual = self.get_virtual_fields(virtual)
        for name, head in virtual.items():
            if name not in names:
                names.append(name)
                header.append(head)

        return header, names

    def get_queryset(self):
        return super().get_queryset().filter(module=self.module)

    def get_base_filename(self):
        return '%s_%s' % (self.project.slug,
                          timezone.now().strftime('%Y%m%dT%H%M%S'))

    def get_header(self):
        return self._header

    def export_rows(self):
        for item in self.get_queryset().all():
            yield [self.get_field_data(item, name) for name in self._names]

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

        # Return the get_field_display value for choice fields
        get_field_display_method = getattr(
            item, 'get_{}_display'.format(name), None)
        if get_field_display_method and callable(get_field_display_method):
            return get_field_display_method()

        # Finally try to get the fields data as a property
        return getattr(item, name, '')

    def get_link_data(self, item):
        return self.request.build_absolute_uri(item.get_absolute_url())

    def get_description_data(self, item):
        return strip_tags(item.description).strip()

    def get_creator_data(self, item):
        return item.creator.username

    def get_created_data(self, item):
        return item.created.isoformat()


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
        return Rating.objects.filter(content_type=ct, value=value).count()


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
                text=strip_tags(comment.comment).strip()
            )

            for reply in comment.child_comments.all():
                yield self.REPLY_FMT.format(
                    date=reply.created.isoformat(),
                    username=reply.creator.username,
                    text=strip_tags(reply.comment).strip()
                )


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


class ItemExportWithModeratorFeedback(VirtualFieldMixin):
    def get_virtual_fields(self, virtual):
        if 'moderator_feedback' not in virtual:
            virtual['moderator_feedback'] = _('Moderator feedback')
        if 'moderator_statement' not in virtual:
            virtual['moderator_statement'] = _('Official Statement')
        return super().get_virtual_fields(virtual)

    def get_moderator_feedback_data(self, item):
        return item.get_moderator_feedback_display()

    def get_moderator_statement_data(self, item):
        if item.moderator_statement:
            return strip_tags(item.moderator_statement.statement).strip()
        return ''
