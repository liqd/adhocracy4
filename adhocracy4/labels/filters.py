import django_filters
from django.utils.translation import gettext_lazy as _

from adhocracy4.filters.widgets import DropdownLinkWidget

from . import models


class LabelFilterWidget(DropdownLinkWidget):
    label = _("Label")

    def __init__(self, *args, **kwargs):
        if "alias" in kwargs:
            self.label = kwargs.pop("alias")
        super().__init__(*args, **kwargs)


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


class LabelAliasFilter(LabelFilter):
    def __init__(self, *args, **kwargs):
        if "widget" not in kwargs:
            if "module" in kwargs:
                module = kwargs.pop("module")
                label_alias = models.LabelAlias.get_label_alias(module)
                if label_alias:
                    kwargs["widget"] = LabelFilterWidget(alias=label_alias.title)
        super().__init__(*args, **kwargs)
