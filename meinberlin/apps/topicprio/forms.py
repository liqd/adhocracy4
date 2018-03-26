from ckeditor_uploader import fields

from adhocracy4.categories.forms import CategorizableFieldMixin
from meinberlin.apps.contrib.mixins import ImageRightOfUseMixin

from . import models


class TopicForm(CategorizableFieldMixin, ImageRightOfUseMixin):

    description = fields.RichTextUploadingFormField(
        config_name='image-editor', required=True)

    class Meta:
        model = models.Topic
        fields = ['name', 'description', 'image', 'category']
