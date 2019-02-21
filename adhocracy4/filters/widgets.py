from itertools import chain

import django_filters
from django.db.models.fields import BLANK_CHOICE_DASH
from django.forms import TextInput
from django.forms.utils import flatatt
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _


class DropdownLinkWidget(django_filters.widgets.LinkWidget):
    """Extend to get a dropdown with links.

    Put 'adhocracy4.filters.apps.FiltersConfig' into your
    settings.

    To use your own template, overwrite the given one.
    """
    label = None
    right = False
    template = 'a4filters/widgets/dropdown_link.html'

    def get_option_label(self, value, choices=()):
        option_label = BLANK_CHOICE_DASH[0][1]

        for v, label in chain(self.choices, choices):
            if str(v) == value:
                option_label = label
                break

        if option_label == BLANK_CHOICE_DASH[0][1]:
            option_label = _('All')

        return option_label

    def render(self, name, value, attrs=None, choices=(), renderer=None):
        all_choices = list(chain(self.choices, choices))

        if len(all_choices) <= 1:
            return ''

        if value is None:
            value = all_choices[0][0]

        _id = attrs.pop('id')
        final_attrs = flatatt(self.build_attrs(attrs))
        value_label = self.get_option_label(value, choices=choices)

        options = super().render(name, value, attrs={
            'class': 'dropdown-menu',
            'aria-labelledby': _id,
        }, choices=choices)

        return render_to_string(self.template, {
            'options': options,
            'id': _id,
            'attrs': final_attrs,
            'value_label': value_label,
            'label': self.label,
            'right': self.right,
        })


class FreeTextFilterWidget(TextInput):
    """This widget renders a complete element. It automatically
    creates hidden fields for all other filters so they are
    preserved on submit.

    Extend to get a text input into your filter.

    Put 'adhocracy4.filters.apps.FiltersConfig' into your
    settings.

    To use your own template, overwrite the given one.
    """
    label = None
    template = 'a4filters/widgets/free_text_filter.html'

    def value_from_datadict(self, data, files, name):
        value = super().value_from_datadict(data, files, name)
        self.data = data
        return value

    def render(self, name, value, attrs=None, renderer=None):
        if not hasattr(self, 'data'):
            self.data = {}
        if value is None:
            value = ''

        _id = attrs.pop('id')

        return render_to_string(self.template, {
            'id': _id,
            'value': value,
            'name': name,
            'label': self.label,
            'url_par': self.data
        })
