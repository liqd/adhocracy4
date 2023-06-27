import django_filters
from django.utils.encoding import force_str
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django_filters.fields import ModelChoiceField

from adhocracy4.filters.widgets import DropdownLinkWidget

from . import get_category_icon_url
from . import has_icons
from . import models


class CategoryFilterWidget(DropdownLinkWidget):
    label = _("Category")

    def __init__(self, *args, **kwargs):
        if "alias" in kwargs:
            self.label = kwargs.pop("alias")
        super().__init__(*args, **kwargs)


class CategoryChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        """
        This method is used to convert objects into strings; it's used to
        generate the labels for the choices presented by this object.
        Subclasses can override this method to customize the display of
        the choices.
        """
        icon_label = ""

        if obj.module and has_icons(obj.module):
            icon_name = getattr(obj, "icon", None)
            icon_url = get_category_icon_url(icon_name)
            icon_label += (
                '<img alt="" class="dropdown-item__icon" src="{icon_src}">'.format(
                    icon_src=force_str(icon_url)
                )
            )

        icon_label += '<span class="dropdown-item__label">{label}</span>'.format(
            label=escape(obj)
        )

        return mark_safe(icon_label)


class CategoryFilter(django_filters.ModelChoiceFilter):
    field_class = CategoryChoiceField

    def __init__(self, *args, **kwargs):
        if "queryset" not in kwargs:
            kwargs["queryset"] = None
        if "widget" not in kwargs:
            kwargs["widget"] = CategoryFilterWidget
        super().__init__(*args, **kwargs)

    def get_queryset(self, request):
        if self.queryset is None:
            return models.Category.objects.filter(module=self.view.module)
        else:
            return super().get_queryset(request)


class CategoryAliasFilter(CategoryFilter):
    def __init__(self, *args, **kwargs):
        if "widget" not in kwargs:
            if "module" in kwargs:
                module = kwargs.pop("module")
                category_alias = models.CategoryAlias.get_category_alias(module)
                if category_alias:
                    kwargs["widget"] = CategoryFilterWidget(alias=category_alias.title)
        super().__init__(*args, **kwargs)
