from ckeditor_uploader import fields
from django import forms
from django.utils.translation import ugettext_lazy as _

from adhocracy4.categories.forms import CategorizableFieldMixin
from adhocracy4.maps import widgets as maps_widgets

from . import models


class MapTopicForm(CategorizableFieldMixin, forms.ModelForm):

    description = fields.RichTextUploadingFormField(
        config_name='image-editor', required=True)

    def __init__(self, *args, **kwargs):
        self.settings = kwargs.pop('settings_instance')
        super().__init__(*args, **kwargs)
        self.fields['point'].widget = maps_widgets.MapChoosePointWidget(
            polygon=self.settings.polygon)
        self.fields['point'].error_messages['required'] = _(
            'Please locate your proposal on the map.')

    class Meta:
        model = models.MapTopic
        fields = ['name', 'description', 'category', 'point', 'point_label']
        labels = {
            'point': _('Locate the place on a map'),
            'point_label': _('Place label'),
        }
