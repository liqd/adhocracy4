from ckeditor_uploader import fields
from django import forms
from django.utils.translation import ugettext_lazy as _

from adhocracy4.categories.forms import CategorizableFieldMixin
from adhocracy4.maps import widgets as maps_widgets

from . import models


class MapTopicForm(CategorizableFieldMixin, forms.ModelForm):

    description = fields.RichTextUploadingFormField(
        config_name='image-editor', required=True)
    right_of_use = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        self.settings = kwargs.pop('settings_instance')
        super().__init__(*args, **kwargs)
        self.fields['point'].widget = maps_widgets.MapChoosePointWidget(
            polygon=self.settings.polygon)
        self.fields['point'].error_messages['required'] = _(
            'Please locate your proposal on the map.')
        if self.instance.image:
            self.initial['right_of_use'] = True

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        right_of_use = cleaned_data.get('right_of_use')
        if image and not right_of_use:
            self.add_error('right_of_use',
                           _("You want to upload an image. "
                             "Please check that you have the "
                             "right of use for the image."))

    class Meta:
        model = models.MapTopic
        fields = ['name', 'description', 'image', 'category',
                  'point', 'point_label']
        labels = {
            'point': _('Locate the place on a map'),
            'point_label': _('Place label'),
        }
