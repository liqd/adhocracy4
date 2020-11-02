from django import forms

from adhocracy4.categories import forms as category_forms

from . import models


class LiveQuestionForm(category_forms.CategorizableFieldMixin,
                       forms.ModelForm):
    class Meta:
        model = models.LiveQuestion
        fields = ['text', 'category']

    def __init__(self, *args, **kwargs):
        self.category_initial = kwargs.pop('category_initial', None)
        super().__init__(*args, **kwargs)
        if self.module.category_set.all():
            self.fields['category'].empty_label = '---'
            if self.category_initial:
                self.initial['category'] = self.category_initial
        else:
            del self.fields['category']


class LiveStreamForm(forms.ModelForm):
    class Meta:
        model = models.LiveStream
        fields = ['live_stream']
