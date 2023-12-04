from django import forms
from django.template.loader import render_to_string


class Select2Mixin:
    def __init__(self, *args, **kwargs):
        if "attrs" not in kwargs:
            kwargs["attrs"] = {}
        if "class" not in kwargs["attrs"]:
            kwargs["attrs"]["class"] = ""
        kwargs["attrs"]["class"] += " js-select2"

        super().__init__(*args, **kwargs)


class Select2Widget(Select2Mixin, forms.Select):
    pass


class TextWithDatalistWidget(forms.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        attrs = self.build_attrs(self.attrs, attrs)
        options = self.get_options(attrs.pop("options"))

        if "list" not in attrs:
            attrs["list"] = attrs["id"] + "_datalist"

        return render_to_string(
            "meinberlin_contrib/text_with_datalist.html",
            {
                "text_input": super().render(name, value, attrs),
                "id_for_datalist": attrs["list"],
                "options": options,
            },
        )

    def get_options(self, options):
        if callable(options):
            return options()
        if options:
            return options
        return {}


class RadioSelectWithTextInputWidget(forms.widgets.MultiWidget):
    """To be used with contrib.fields.ChoiceWithOtherOptionField."""

    def __init__(self, choices, placeholder_textinput="", *args, **kwargs):
        self.choices = choices
        widgets = (
            forms.RadioSelect(choices=choices),
            forms.TextInput(attrs={"placeholder": placeholder_textinput}),
        )
        super(RadioSelectWithTextInputWidget, self).__init__(widgets, *args, **kwargs)

    def decompress(self, value):
        # inital
        if not value:
            return [self.choices[0][0], ""]
        # if 'other' was chosen
        elif value not in [val for (val, label) in self.choices]:
            return ["other", value]
        else:
            return [value, ""]
