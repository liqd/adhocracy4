from django.contrib.staticfiles.storage import staticfiles_storage
from django.forms import widgets
from django.utils import formats
from django.utils.safestring import mark_safe
from django.utils.translation import get_language


class DateInput(widgets.DateInput):
    class Media:
        js = (staticfiles_storage.url('flatpickr.min.js'),
              staticfiles_storage.url('js/dateTimeInput.js'))
        css = {'all': [staticfiles_storage.url('flatpickr.min.css')]}

    input_type = 'text'
    format_index = 0

    # becomes a public value in Django 1.10
    def _format_value(self, value):
        return value

    def render(self, name, value, attrs=None):
        if attrs:
            format = formats.get_format(
                self.format_key
            )[self.format_index]
            attrs.update({
                'class': attrs.get('class', '') + ' flatpickr',
                'data-language': get_language(),
                'data-alt-format': format.replace('%', '').replace('M', 'i'),
                'data-date-format': format.replace('%', '').replace('M', 'i'),
            })

            if hasattr(self, 'additional_attrs'):
                attrs.update(self.additional_attrs)

            if value:
                attrs.update({
                    'data-default-date': value
                })
        input = mark_safe(super().render(name, value, attrs))

        return input


class DateTimeInput(DateInput):

    additional_attrs = {
        'data-time_24hr': 'true',
        'data-enable-time': 'true',
        'data-alt-input': 'true'
    }

    format_index = 2
    format_key = 'DATETIME_INPUT_FORMATS'
