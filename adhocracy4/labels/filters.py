import django_filters
from django.utils.translation import gettext_lazy as _

from adhocracy4.filters.widgets import DropdownLinkWidget

from . import models


class LabelFilterWidget(DropdownLinkWidget):
    label = _("Label")


class LabelFilter(django_filters.ModelChoiceFilter):
    def __init__(self, *args, **kwargs):
        if "queryset" not in kwargs:
            kwargs["queryset"] = None
        if "widget" not in kwargs:
            kwargs["widget"] = LabelFilterWidget
        super().__init__(*args, **kwargs)

    def get_queryset(self, request):
        if self.queryset is None:
            return models.Label.objects.filter(module=self.view.module)
        else:
            return super().get_queryset(request)
