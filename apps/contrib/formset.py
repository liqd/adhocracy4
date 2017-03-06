from django import forms


class DynamicModelFormSet(forms.BaseModelFormSet):
    @property
    def media(self):
        additional_js = forms.Media(js={
            'js/formset.js'
        })
        return super().media + additional_js


def dynamic_modelformset_factory(*args, **kwargs):
    kwargs.update({
        'formset': DynamicModelFormSet
    })
    modelformset = forms.modelformset_factory(*args, **kwargs)

    return modelformset
