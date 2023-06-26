from django import forms
from django.utils.translation import gettext_lazy as _

# Mixin to ensure image cannot be saved without adding meta data


class ImageMetadataMixin(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Delete meta data when image deleted
        if not self.instance.image:
            self.initial["image_copyright"] = None
            self.initial["image_alt_text"] = None
        if not self.instance.tile_image:
            self.initial["tile_image_copyright"] = None
            self.initial["tile_image_alt_text"] = None

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get("image")
        tile_image = cleaned_data.get("tile_image")
        image_copyright = cleaned_data.get("image_copyright")
        tile_image_copyright = cleaned_data.get("tile_image_copyright")
        image_alt_text = cleaned_data.get("image_alt_text")
        tile_image_alt_text = cleaned_data.get("tile_image_alt_text")
        if image and not image_copyright:
            self.add_error(
                "image_copyright",
                _("Please add copyright information."),
            )
        if tile_image and not tile_image_copyright:
            self.add_error(
                "tile_image_copyright",
                _("Please add copyright information."),
            )
        if image and not image_alt_text:
            self.add_error(
                "image_alt_text",
                _("Please add an alternative text for this image"),
            )
        if tile_image and not tile_image_alt_text:
            self.add_error(
                "tile_image_alt_text",
                _("Please add an alternative text for this image"),
            )
        return cleaned_data
