from collections import OrderedDict
import xlsxwriter

from django.views import generic
from django.core.exceptions import FieldError
from django.http import HttpResponse
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.translation import ugettext as _

from .mixins import VirtualFieldMixin




class AbstractXlsxExportView(generic.View):

    def get_filename(self):
        project = self.module.project
        filename = '%s_%s.xlsx' % (project.slug,
                                   timezone.now().strftime('%Y%m%dT%H%M%S'))
        return filename

    def get(self, request, *args, **kwargs):
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument'
                         '.spreadsheetml.sheet')
        response['Content-Disposition'] = \
            'attachment; filename="%s"' % self.get_filename()

        workbook = xlsxwriter.Workbook(response, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        for col, field in enumerate(self.get_header()):
            worksheet.write(0, col, field)

        for rownum, row in enumerate(self.export_rows(), start=1):
            for col, field in enumerate(row):
                worksheet.write(rownum, col, field)

        workbook.close()

        return response


class ItemExportView(AbstractXlsxExportView,
                     VirtualFieldMixin,
                     generic.list.MultipleObjectMixin):
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
