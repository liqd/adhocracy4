from django import forms
from django.contrib.staticfiles.storage import staticfiles_storage


class Select2Mixin:
    def __init__(self, *args, **kwargs):
        if 'attrs' not in kwargs:
            kwargs['attrs'] = {}
        if 'class' not in kwargs['attrs']:
            kwargs['attrs']['class'] = ''
        kwargs['attrs']['class'] += ' js-select2'

        super().__init__(*args, **kwargs)

    class Media:
        js = (
            staticfiles_storage.url('select2.js'),
        )


class Select2Widget(Select2Mixin, forms.Select):
    pass


class Select2MultipleWidget(Select2Mixin, forms.SelectMultiple):
    pass
