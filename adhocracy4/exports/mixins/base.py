from adhocracy4.exports import unescape_and_strip_html


class VirtualFieldMixin:
    def get_virtual_fields(self, virtual):
        return virtual


class ExportModelFieldsMixin(VirtualFieldMixin):
    """
    Adds fields that are specified in the export.

    Requires self.model to be set. If fields are set, only these are
    exported, if excluse is set, all fields apart from these are exported.
    If neither are set, all model fields are exported. html_fields are
    treated differently and need to be added to the export with the above
    options as well as to the html_fields.
    """
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
