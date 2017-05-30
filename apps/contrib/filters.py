import django_filters
from django.utils.translation import ugettext_lazy

from adhocracy4.categories import models as category_models

from . import mixins
from . import widgets


def category_queryset(request):
    return category_models.Category.objects.filter(module=request.module)


class CategoryFilterWidget(widgets.DropdownLinkWidget):
    label = ugettext_lazy('Category')


class CategoryFilter(django_filters.ModelChoiceFilter):

    def __init__(self, *args, **kwargs):
        if 'queryset' not in kwargs:
            kwargs['queryset'] = category_queryset
        if 'widget' not in kwargs:
            kwargs['widget'] = CategoryFilterWidget
        super().__init__(*args, **kwargs)


class OrderingWidget(widgets.DropdownLinkWidget):
    label = ugettext_lazy('Ordering')
    right = True


class OrderingFilter(mixins.ChoicesRequestMixin,
                     django_filters.OrderingFilter):

    def __init__(self, *args, **kwargs):
        if 'widget' not in kwargs:
            kwargs['widget'] = OrderingWidget
        kwargs['empty_label'] = None
        super().__init__(*args, **kwargs)
