from django.db import models
from django.db.models.fields import files as django_fields
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.text import format_lazy
from easy_thumbnails.files import get_thumbnailer

from adhocracy4.files.fields import ConfiguredFileField
from . import forms, validators


class ConfiguredImageFieldFile(django_fields.ImageFieldFile):
    def delete(self, save=True):
        thumbnailer = get_thumbnailer(self)
        thumbnailer.delete_thumbnails()
        super().delete(save)


class ConfiguredImageField(ConfiguredFileField):
    attr_class = ConfiguredImageFieldFile
    form_class = forms.ImageField

    @property
    def validators(self):
        default_validators = super().validators
        image_validators = [
            lambda image: validators.validate_image(image, self.file_config)
        ]
        image_validators.extend(default_validators)
        return image_validators

    @property
    def file_config(self):
        c = {}
        defaults = settings.IMAGE_ALIASES.get('*', {})
        c.update(defaults)
        c.update(settings.IMAGE_ALIASES[self.config_name])
        return c

    @property
    def _help_text(self):
        config = self.file_config

        help_text = format_lazy(
            _(
                '{help_prefix} It must be min. {min_resolution[0]} pixel wide '
                'and {min_resolution[1]} pixel tall. Allowed file formats are '
                '{fileformats_str}. The file size should be max. '
                '{max_size_mb} MB.'
            ),
            help_prefix=self.help_prefix,
            max_size_mb=int(config['max_size']/(10**6)),
            fileformats_str=', '.join(
                name for name, _ in config['fileformats']
            ),
            **config
        )
        return help_text


class ImageCopyrightField(models.CharField):

    def __init__(self, *args, image_name='image', **kwargs):
        defaults = {
            'verbose_name': format_lazy(
                _('{image_name} copyright'),
                image_name=image_name),
            'help_text': format_lazy(
                _('Copyright shown in the {image_name}.'),
                image_name=image_name),
            'max_length': 120,
            'blank':  True,
        }
        defaults.update(kwargs)
        super().__init__(*args, **defaults)
