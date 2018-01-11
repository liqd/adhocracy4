from collections import OrderedDict
import xlsxwriter

from django.views import generic
from django.http import HttpResponse
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.translation import ugettext as _

from .mixins import VirtualFieldMixin


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


class SimpleItemExportView(AbstractXlsxExportView,
                           VirtualFieldMixin):

    def __init__(self):
        super().__init__()
        self._header, self._names = self._setup_fields()

    def _setup_fields(self):
        raise NotImplementedError

    def get_header(self):
        return self._header

    def export_rows(self):
        raise NotImplementedError

    def get_base_filename(self):
        return '%s_%s' % ('download',
                          timezone.now().strftime('%Y%m%dT%H%M%S'))

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
        return str(getattr(item, name, ''))

    def get_link_data(self, item):
        return self.request.build_absolute_uri(item.get_absolute_url())

    def get_description_data(self, item):
        return strip_tags(item.description).strip()

    def get_creator_data(self, item):
        return item.creator.username

    def get_created_data(self, item):
        return item.created.isoformat()


class ItemExportView(SimpleItemExportView,
                     generic.list.MultipleObjectMixin):
    fields = None
    exclude = None
    model = None

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

    def get_base_filename(self):
        return '%s_%s' % (self.project.slug,
                          timezone.now().strftime('%Y%m%dT%H%M%S'))

    def get_queryset(self):
        qs = super().get_queryset()
        if hasattr(self, 'module') and self.module:
            qs = qs.filter(module=self.module)
        return qs

    def export_rows(self):
        for item in self.get_queryset().all():
            yield [self.get_field_data(item, name) for name in self._names]
