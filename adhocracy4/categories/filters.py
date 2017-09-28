import django_filters
from django.utils.translation import ugettext_lazy as _

from adhocracy4.filters.widgets import DropdownLinkWidget

from . import models


def category_queryset(request):
    return models.Category.objects.filter(
        module=request.module)


class CategoryFilterWidget(DropdownLinkWidget):
    label = _('Category')


class CategoryFilter(django_filters.ModelChoiceFilter):

    def __init__(self, *args, **kwargs):
        if 'queryset' not in kwargs:
            kwargs['queryset'] = category_queryset
        if 'widget' not in kwargs:
            kwargs['widget'] = CategoryFilterWidget
        super().__init__(*args, **kwargs)
