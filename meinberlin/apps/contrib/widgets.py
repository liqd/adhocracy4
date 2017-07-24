import datetime

from django.contrib.staticfiles.storage import staticfiles_storage
from django.forms import widgets as form_widgets
from django.template.loader import render_to_string
from django.utils import formats
from django.utils.timezone import localtime


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
