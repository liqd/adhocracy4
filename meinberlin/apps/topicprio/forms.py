from django import forms
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from adhocracy4.categories.forms import CategorizableFieldMixin
from adhocracy4.labels.mixins import LabelsAddableFieldMixin
from meinberlin.apps.contrib.mixins import CategoryAndLabelAliasMixin
from meinberlin.apps.contrib.widgets import Select2Widget

from . import models


class TopicForm(
    CategorizableFieldMixin,
    LabelsAddableFieldMixin,
    CategoryAndLabelAliasMixin,
    forms.ModelForm,
):
    description = CKEditor5Field(config_name="image-editor")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].label = _("Description")

    class Meta:
        model = models.Topic
        fields = ["name", "description", "category", "labels"]
        widgets = {"category": Select2Widget(attrs={"class": "select2__no-search"})}
