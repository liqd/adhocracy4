from ckeditor_uploader import fields
from django import forms

from adhocracy4.categories.forms import CategorizableFieldMixin
from adhocracy4.labels.mixins import LabelsAddableFieldMixin

from . import models


class TopicForm(CategorizableFieldMixin,
                LabelsAddableFieldMixin,
                forms.ModelForm):

    description = fields.RichTextUploadingFormField(
        config_name='image-editor', required=True)

    class Meta:
        model = models.Topic
        fields = ['name', 'description', 'category', 'labels']
