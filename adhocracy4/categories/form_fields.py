from django import forms
from django.conf import settings
from django.forms import widgets

from adhocracy4.categories import get_category_icon_url


class CategorySelectWidget(widgets.Select):
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        current_class = context["widget"]["attrs"].get("class", "")
        new_class = current_class + " select-dropdown"

        context["widget"]["attrs"]["class"] = new_class
        return context

    def create_option(self, name, value, label, selected, index, **kwargs):
        option = super().create_option(name, value, label, selected, index, **kwargs)
        if value in self.icons:
            icon_url = get_category_icon_url(value)
            option["attrs"]["data-icon-src"] = icon_url

        return option


class CategoryChoiceField(forms.ChoiceField):
    widget = CategorySelectWidget

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.icons = self.icons
        self.choices = getattr(settings, "A4_CATEGORY_ICONS", [])

    @property
    def icons(self):
        return dict(self.choices)


class IconSelectWidget(widgets.Select):
    def create_option(self, name, value, label, selected, index, **kwargs):
        option = super().create_option(name, value, label, selected, index, **kwargs)

        icon_url = get_category_icon_url(value)
        option["attrs"]["data-icon-src"] = icon_url
        return option


class IconChoiceField(forms.TypedChoiceField):
    widget = IconSelectWidget
