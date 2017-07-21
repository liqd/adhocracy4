from collections import OrderedDict

import multiform
from django.forms import formsets


class MultiModelForm(multiform.MultiModelForm):

    def __init__(self, *args, **kwargs):
        """Filter arguments that don't make sense for formsets as base_forms.

        Should be moved to multiforms itself.
        """
        base_forms = self.get_base_forms()
        formset_names = [name for name, form in base_forms.items()
                         if issubclass(form, formsets.BaseFormSet)]

        invalid_formset_kwargs = [
            'instance', 'empty_permitted', 'label_suffix'
        ]

        def filter_function(name, value):
            if name in formset_names:
                return multiform.InvalidArgument
            else:
                return value

        for kwarg in invalid_formset_kwargs:
            setattr(self, 'dispatch_init_{}'.format(kwarg), filter_function)

        return super().__init__(*args, **kwargs)

    def _combine(self, *args, **kwargs):
        """Combine with filter argument doesn't work for form sets.

        Because formsets will return always a list of values and even lists of
        falsy values are truthy.

        This extends combine to inside the lists returned by the formset and
        filter it if all values inside are false.

        WARNING: This kind of hacky. It should be better fixed somewhere else.
        """
        base_forms = self.get_base_forms()
        values = super()._combine(*args, **kwargs)
        if 'filter' in kwargs and kwargs['filter']:
            values = OrderedDict([
                (name, value) for name, value in values.items()
                if not issubclass(base_forms[name], formsets.BaseFormSet) or
                any(value)
            ])
        return values

    def full_clean(self):
        """Do full clean and collect cleaned data from formsets.

        Should be moved to multiforms itself.
        """
        self._errors = self._combine('errors', filter=True)
        base_forms = self.get_base_forms()

        if not self._errors:
            self.cleaned_data = {}
            for name, formset in self.forms.items():
                if issubclass(base_forms[name], formsets.BaseFormSet):
                    self.cleaned_data[name] = [f.cleaned_data for f in formset]

    def get_formset(self, formset_name):
        for name, formset in self.forms.items():
            if name == formset_name:
                return formset
