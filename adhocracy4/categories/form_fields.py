from collections import abc

from django import forms
from django.forms import widgets
from django.utils.functional import cached_property

from adhocracy4.categories import get_category_icon_url


class CategoryIconDict(abc.Mapping):
    def __init__(self, field):
        self.field = field
        self.queryset = field.queryset

    @cached_property
    def _icons(self):
        return {
            self.field.prepare_value(obj): getattr(obj, 'icon', None)
            for obj in self.queryset.all()
        }

    def __getitem__(self, key):
        return self._icons.__getitem__(key)

    def __iter__(self):
        return self._icons.__iter__()

    def __len__(self):
        return self._icons.__len__()


class CategorySelectWidget(widgets.Select):
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        current_class = context['widget']['attrs'].get('class', '')
        new_class = current_class + ' select-dropdown'

        context['widget']['attrs']['class'] = new_class
        return context

    def create_option(self, name, value, label, selected, index, **kwargs):
        option = super().create_option(name, value, label, selected, index,
                                       **kwargs)
        if value and value in self.icons:
            icon_url = get_category_icon_url(self.icons[value])
            option['attrs']['data-icon-src'] = icon_url

        return option


class CategoryChoiceField(forms.ModelChoiceField):
    widget = CategorySelectWidget

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.icons = self.icons

    @property
    def icons(self):
        return CategoryIconDict(self)

    # Update the icons if the queryset is updated
    def _set_queryset(self, queryset):
        super()._set_queryset(queryset)
        self.widget.icons = self.icons

    queryset = property(forms.ModelChoiceField._get_queryset, _set_queryset)


class IconSelectWidget(widgets.Select):
    def create_option(self, name, value, label, selected, index, **kwargs):
        option = super().create_option(name, value, label, selected, index,
                                       **kwargs)

        icon_url = get_category_icon_url(value)
        option['attrs']['data-icon-src'] = icon_url
        return option


class IconChoiceField(forms.TypedChoiceField):
    widget = IconSelectWidget
