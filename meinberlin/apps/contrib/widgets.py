import datetime
from itertools import chain

import django_filters
from django.contrib.staticfiles.storage import staticfiles_storage
from django.db.models.fields import BLANK_CHOICE_DASH
from django.forms import widgets as form_widgets
from django.forms.widgets import flatatt
from django.template.loader import render_to_string
from django.utils import formats
from django.utils.timezone import localtime
from django.utils.translation import ugettext as _


class DropdownLinkWidget(django_filters.widgets.LinkWidget):
    label = None
    right = False
    template = 'meinberlin_contrib/widgets/dropdown_link.html'

    def get_option_label(self, value, choices=()):
        option_label = BLANK_CHOICE_DASH[0][1]

        for v, label in chain(self.choices, choices):
            if str(v) == value:
                option_label = label
                break

        if option_label == BLANK_CHOICE_DASH[0][1]:
            option_label = _('All')

        return option_label

    def render(self, name, value, attrs=None, choices=()):
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


class DateTimeInput(form_widgets.SplitDateTimeWidget):
    class Media:
        js = (
            staticfiles_storage.url('datepicker.js'),
        )
        css = {'all': [
            staticfiles_storage.url('datepicker.css'),
        ]}

    def render(self, name, value, attrs=None):
        date_attrs = self.build_attrs(attrs)
        date_attrs.update({
            'class': 'datepicker',
            'placeholder': formats.localize_input(datetime.date.today()),
            'id': name + '_date'
        })
        time_attrs = self.build_attrs(attrs)
        time_attrs.update({
            'class': 'timepicker',
            'placeholder': '00:00',
            'id': name + '_time'
        })

        if isinstance(value, datetime.datetime):
            value = localtime(value)
            date = value.date()
            time = value.time()
        else:
            # value's just a list in case of an error
            date = value[0] if value else None
            time = value[1] if value else '00:00'

        return render_to_string('datetime_input.html', {
            'date': self.widgets[0].render(
                name + '_0',
                date,
                date_attrs
            ),
            'time': self.widgets[1].render(
                name + '_1',
                time,
                time_attrs
            )
        })
