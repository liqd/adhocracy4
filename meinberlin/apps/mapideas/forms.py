from django import forms
from django.utils.translation import ugettext_lazy as _

from adhocracy4.categories.forms import CategorizableFieldMixin
from adhocracy4.maps import widgets as maps_widgets

from . import models


class MapIdeaForm(CategorizableFieldMixin, forms.ModelForm):
    right_of_use = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        self.settings = kwargs.pop('settings_instance')
        super().__init__(*args, **kwargs)
        self.fields['point'].widget = maps_widgets.MapChoosePointWidget(
            polygon=self.settings.polygon)
        self.fields['point'].error_messages['required'] = _(
            'Please locate your proposal on the map.')
        if self.instance.name != '' and self.instance.image:
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

    class Media:
        js = ('js/select_dropdown_init.js',)

    class Meta:
        model = models.MapIdea
        fields = ['name', 'description', 'image', 'category',
                  'point', 'point_label']


class MapIdeaModerateForm(forms.ModelForm):
    class Meta:
        model = models.MapIdea
        fields = ['moderator_feedback']
