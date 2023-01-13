from django import forms
from django.utils.translation import gettext_lazy as _

from adhocracy4.categories.forms import CategorizableFieldMixin
from adhocracy4.labels.mixins import LabelsAddableFieldMixin
from adhocracy4.maps import widgets as maps_widgets
from meinberlin.apps.contrib.mixins import ImageRightOfUseMixin
from meinberlin.apps.contrib.widgets import Select2Widget

from . import models


class MapIdeaForm(
    CategorizableFieldMixin, LabelsAddableFieldMixin, ImageRightOfUseMixin
):
    def __init__(self, *args, **kwargs):
        self.settings = kwargs.pop("settings_instance")
        super().__init__(*args, **kwargs)
        self.fields["point"].widget = maps_widgets.MapChoosePointWidget(
            polygon=self.settings.polygon
        )
        self.fields["point"].error_messages["required"] = _(
            "Please locate your proposal on the map."
        )

    class Meta:
        model = models.MapIdea
        fields = [
            "name",
            "description",
            "image",
            "category",
            "labels",
            "point",
            "point_label",
        ]
        widgets = {"category": Select2Widget(attrs={"class": "select2__no-search"})}


class MapIdeaModerateForm(forms.ModelForm):
    class Meta:
        model = models.MapIdea
        fields = ["moderator_status"]
