from django import forms


def _make_fields_required(fields, required):
    """Set the required attributes on all fields who's key is in required."""
    if required:
        for name, field in fields:
            if required == '__all__' or name in required:
                field.required = True


def _make_fields_required_for_publish(fields, required):
    """Set the required attributes on all fields who's key is in required."""
    if required:
        for name, field in fields:
            if required == '__all__' or name in required:
                field.required_for_publish = True


class ProjectDashboardForm(forms.ModelForm):
    """
    Base form for project related dashboard forms.

    Sets fields to required if the project is published.
    Intended to be used with ProjectFormComponent's.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.get_project().is_draft:
            _make_fields_required(self.fields.items(),
                                  self.get_required_fields())

        _make_fields_required_for_publish(self.fields.items(),
                                          self.get_required_fields())

    def get_project(self):
        return self.instance

    @classmethod
    def get_required_fields(cls):
        meta = getattr(cls, 'Meta', None)
        return getattr(meta, 'required_for_project_publish', [])


class ModuleDashboardForm(forms.ModelForm):
    """
    Base form for module related dashboard forms.

    Sets fields to required if the project is published.
    Intended to be used with ModuleFormComponent's.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.get_project().is_draft:
            _make_fields_required(self.fields.items(),
                                  self.get_required_fields())

        _make_fields_required_for_publish(self.fields.items(),
                                          self.get_required_fields())

    def get_project(self):
        return self.instance.project

    @classmethod
    def get_required_fields(cls):
        meta = getattr(cls, 'Meta', None)
        return getattr(meta, 'required_for_project_publish', [])


class ModuleDashboardFormSet(forms.BaseInlineFormSet):
    """
    Base form for module related dashboard formsets.

    Sets fields to required if the project is published.
    Intended to be used with ModuleFormSetComponent's.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        required_fields = self.get_required_fields()
        for form in self.forms:
            _make_fields_required_for_publish(form.fields.items(),
                                              required_fields)
            if not self.instance.project.is_draft:
                _make_fields_required(form.fields.items(),
                                      required_fields)

    def get_project(self):
        return self.instance.project

    @classmethod
    def get_required_fields(cls):
        meta = getattr(cls.form, 'Meta', None)
        return getattr(meta, 'required_for_project_publish', [])
