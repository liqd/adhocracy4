from django.forms.fields import SplitDateTimeField
from django.utils.translation import ugettext_lazy as _

from .widgets import DateTimeInput


class DateTimeField(SplitDateTimeField):
    widget = DateTimeInput

    def __init__(self, date_format=None, time_format=None, time_default=None,
                 *args, **kwargs):
        label = kwargs.get('label', None)
        time_label = ''
        if type(label) == tuple:
            date_label, time_label = label
            kwargs['label'] = date_label
        elif label:
            time_label = _('Time of %(date_label)s' % {'date_label': label})

        if 'widget' not in kwargs:
            kwargs['widget'] = self.widget(date_format=date_format,
                                           time_format=time_format,
                                           time_label=time_label,
                                           time_default=time_default)

        super().__init__(*args, **kwargs)

    def clean(self, value):
        value = self._set_default_time(value)
        return super().clean(value)

    def bound_data(self, data, initial):
        # If both fields are empty, set the data to None
        # This allows to mark required for publish fields
        if data == ['', '']:
            return None

        data = self._set_default_time(data)
        return super().bound_data(data, initial)

    def _set_default_time(self, value):
        # Set the default time if only a date is submitted
        if isinstance(value, (list, tuple)):
            date, time = value
            if (not self.require_all_fields and
                    time in self.empty_values and
                    date not in self.empty_values):
                value[1] = self.widget.get_default_time()
        return value
