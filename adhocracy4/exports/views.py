import numbers
from collections import OrderedDict

import xlsxwriter
from django.http import HttpResponse
from django.utils import timezone
from django.views import generic

from adhocracy4.projects.mixins import ProjectMixin

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


class BaseExport(VirtualFieldMixin):

    def get_fields(self):
        # Get virtual fields in their order from the Mixins
        header = []
        names = []

        virtual = OrderedDict()
        virtual = self.get_virtual_fields(virtual)
        for name, head in virtual.items():
            if name not in names:
                names.append(name)
                header.append(head)

        return names, header

    def get_header(self):
        _, header = self.get_fields()
        return header

    def export_rows(self):
        names, _ = self.get_fields()

        for item in self.get_object_list():
            yield [self.get_field_data(item, name) for name in names]

    def get_field_data(self, item, name):
        # Use custom getters if they are defined
        get_field_attr_name = 'get_%s_data' % name
        if hasattr(self, get_field_attr_name):
            get_field_attr = getattr(self, get_field_attr_name)

            if hasattr(get_field_attr, '__call__'):
                return get_field_attr(item)
            return get_field_attr

        # Finally try to get the fields data as a property
        value = getattr(item, name, '')
        if isinstance(value, numbers.Number) and not isinstance(value, bool):
            return value
        elif value is None:
            return ''
        return str(value)


class BaseItemExportView(BaseExport,
                         ProjectMixin,
                         generic.list.MultipleObjectMixin,
                         AbstractXlsxExportView):

    def get_queryset(self):
        return super().get_queryset().filter(module=self.module)

    def get_object_list(self):
        return self.get_queryset().all()

    def get_base_filename(self):
        return '%s_%s' % (self.project.slug,
                          timezone.now().strftime('%Y%m%dT%H%M%S'))
