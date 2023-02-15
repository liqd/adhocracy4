from adhocracy4.exports import unescape_and_strip_html


class VirtualFieldMixin:
    def get_virtual_fields(self, virtual):
        return virtual


class ExportModelFieldsMixin(VirtualFieldMixin):
    """
    Adds fields that are specified in the export.

    Requires self.model to be set. If fields are set, only these are
    exported, if exclude is set, all fields apart from these are exported.
    If neither are set, all model fields are exported. html_fields are
    treated differently and need to be added to the export with the above
    options as well as to the html_fields. related_fields is an optional
    dictionary {related_field: [related_field_attr]} to specify which
    attributes of a related_field should be exported, e.g. {'organisation':
    ['id', 'name']}. The related field also needs to be added to fields
    and if there is no related_fields entry for it, the string representation
    of it will be exported.
    """

    fields = None
    exclude = None
    html_fields = None
    related_fields = None
    choice_fields = None

    def get_virtual_fields(self, virtual):
        meta = self.model._meta
        exclude = self.exclude if self.exclude else []

        if self.fields:
            fields = [meta.get_field(name) for name in self.fields]
        else:
            fields = meta.get_fields()

        for field in fields:
            if (
                field.concrete
                and not (field.one_to_one and field.remote_field.parent_link)
                and field.name not in exclude
                and field.name not in virtual
            ):
                if self.related_fields and field.name in self.related_fields:
                    for attr in self.related_fields[field.name]:
                        related_field_name = "%s_%s" % (field.name, attr)
                        virtual[related_field_name] = related_field_name
                else:
                    virtual[field.name] = str(field.verbose_name)

        self._setup_html_fields()
        self._setup_related_fields()
        self._setup_choice_fields()

        return super().get_virtual_fields(virtual)

    def _setup_html_fields(self):
        html_fields = self.html_fields if self.html_fields else []
        for field in html_fields:
            get_field_attr_name = "get_%s_data" % field
            setattr(
                self,
                get_field_attr_name,
                lambda item, field_name=field: unescape_and_strip_html(
                    getattr(item, field_name)
                ),
            )

    def _setup_related_fields(self):
        related_fields = self.related_fields if self.related_fields else {}
        for field in related_fields:
            for attr in related_fields[field]:
                get_field_attr_name = "get_%s_%s_data" % (field, attr)
                setattr(
                    self,
                    get_field_attr_name,
                    lambda item, field=field, attr=attr: str(
                        getattr(getattr(item, field), attr, "")
                    ),
                )

    def _setup_choice_fields(self):
        choice_fields = self.choice_fields if self.choice_fields else []
        for field in choice_fields:
            get_field_attr_name = "get_%s_data" % field
            setattr(
                self,
                get_field_attr_name,
                lambda item, field_name_display="get_%s_display" % field: str(
                    getattr(item, field_name_display)()
                ),
            )
