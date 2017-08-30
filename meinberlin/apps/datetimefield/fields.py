from django.forms.fields import SplitDateTimeField
from django.utils.translation import ugettext_lazy as _

from .widgets import DateTimeInput


class DateTimeField(SplitDateTimeField):
    widget = DateTimeInput

    def __init__(self, date_format=None, time_format=None,
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
                                           time_label=time_label)

        super().__init__(*args, **kwargs)

    def clean(self, value):
        pass
