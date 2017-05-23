from django import forms


class ItemForm(forms.ModelForm):
    """
    Base form for items indented to use together with Item*Views.
    """

    def __init__(self, *args, **kwargs):
        self.module = kwargs.pop('module', None)
        self.settings_instance = kwargs.pop('settings_instance', None)
        super(ItemForm, self).__init__(*args, **kwargs)
