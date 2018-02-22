import django_filters
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
from django_filters.fields import ModelChoiceField
from django.utils.safestring import mark_safe

from adhocracy4.filters.widgets import DropdownLinkWidget

from . import models


class CategoryFilterWidget(DropdownLinkWidget):
    label = _('Category')

    def get_option_label(self, value, choices=()):
        option_label = super().get_option_label(value, choices=())

        # Probably not the best idea!
        return mark_safe(option_label)


class CategoryChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        """
        This method is used to convert objects into strings; it's used to
        generate the labels for the choices presented by this object. Subclasses
        can override this method to customize the display of the choices.
        """
        icon_name = obj.icon if hasattr(obj, 'icon') else 'default'
        icon_src = static('category_icons/icons/{}_icon.svg'.format(icon_name))

        icon_label = \
            '<img class="dropdown-item__icon" src="{icon_src}">' \
            '<span class="dropdown-item__label">{label}</span>' \
            .format(icon_src=icon_src, label=force_text(obj))

        return icon_label


class CategoryFilter(django_filters.ModelChoiceFilter):
    field_class = CategoryChoiceField

    def __init__(self, *args, **kwargs):
        if 'queryset' not in kwargs:
            kwargs['queryset'] = None
        if 'widget' not in kwargs:
            kwargs['widget'] = CategoryFilterWidget
        super().__init__(*args, **kwargs)

    def get_queryset(self, request):
        if self.queryset is None:
            return models.Category.objects.filter(
                module=self.view.module
            )
        else:
            return super().get_queryset(request)


