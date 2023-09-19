from django import forms
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from adhocracy4.categories.forms import CategorizableFieldMixin
from adhocracy4.labels.mixins import LabelsAddableFieldMixin
from adhocracy4.maps import widgets as maps_widgets
from meinberlin.apps.contrib.mixins import CategoryAndLabelAliasMixin

from . import models


class MapTopicForm(
    CategorizableFieldMixin,
    LabelsAddableFieldMixin,
    CategoryAndLabelAliasMixin,
    forms.ModelForm,
):
    description = CKEditor5Field(config_name="image-editor")

    def __init__(self, *args, **kwargs):
        self.settings = kwargs.pop("settings_instance")
        super().__init__(*args, **kwargs)
        self.fields["point"].widget = maps_widgets.MapChoosePointWidget(
            polygon=self.settings.polygon
        )
        self.fields["point"].error_messages["required"] = _(
            "Please locate your proposal on the map."
        )
        self.fields["description"].label = _("Description")

    class Meta:
        model = models.MapTopic
        fields = ["name", "description", "category", "labels", "point", "point_label"]
        labels = {
            "point": _("Locate the place on a map"),
            "point_label": _("Place label"),
        }
