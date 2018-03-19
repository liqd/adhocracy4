from django.forms import fields as django_fields

from . import widgets


class FileField(django_fields.FileField):
    widget = widgets.FileInputWidget
