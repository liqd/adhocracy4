from django.forms.fields import ImageField

from . import widgets


class ImageField(ImageField):
    widget = widgets.ImageInputWidget
