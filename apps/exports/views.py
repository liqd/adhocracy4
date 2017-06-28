import csv

from django.core.exceptions import FieldError
from django.http import HttpResponse
from django.utils.translation import ugettext as _

from adhocracy4.modules import views as module_views


class ItemExportView(module_views.ItemListView):
    paginate_by = 0
    fields = None
    exclude = None
    virtual = None
    model = None

    def __init__(self):
        super(ItemExportView, self).__init__()
        if self.fields and self.exclude:
            raise FieldError()
        self._header, self._names = self._setup_fields()

    def _setup_fields(self):
        meta = self.model._meta

        if self.fields:
            fields = [meta.get_field(name) for name in self.fields]
        else:
            fields = meta.get_fields()

        names = ['link']
        header = [_('Link')]
        for field in fields:
            if field.concrete \
                    and not (field.one_to_one and field.rel.parent_link) \
                    and field.attname not in self.exclude \
                    and field.attname not in names:

                names.append(field.attname)
                header.append(str(field.verbose_name))

        if self.virtual:
            for head, name in self.virtual:
                if name not in names:
                    names.append(name)
                    header.append(head)

        return header, names

    def get_queryset(self):
        return super().get_queryset()

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
        if name in item:
            return item['name']

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
