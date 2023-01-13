from django import forms


class ChoiceWithOtherOptionField(forms.MultiValueField):
    """Custom choice field with extra char field.

    To be used with contrib.widgets.RadioSelectWithTextInputWidget.
    Choices' last option needs to be of the form ('other', some_label),
    if 'other' is chosen, the value entered in the text input will
    be submitted.
    """

    def __init__(self, choices, validators_textinput=[], **kwargs):
        fields = (
            forms.ChoiceField(required=False, choices=choices),
            forms.CharField(required=False, validators=validators_textinput),
        )
        super().__init__(fields=fields, require_all_fields=False, **kwargs)

    def compress(self, value):
        if not value:
            return ""
        else:
            val_option, val_text = value
            if val_option == "other":
                return val_text
            else:
                return val_option
