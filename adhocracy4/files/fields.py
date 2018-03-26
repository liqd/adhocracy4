from django.db.models.fields import files as django_fields
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.text import format_lazy

from . import forms, validators


class ConfiguredFileField(django_fields.FileField):
    form_class = forms.FileField

    def __init__(self, config_name, *args, **kwargs):
        defaults = {}
        self.config_name = config_name

        if 'help_prefix' in kwargs:
            self.help_prefix = kwargs['help_prefix']
            del kwargs['help_prefix']
            defaults['help_text'] = self._help_text
        else:
            self.help_prefix = None

        defaults.update(kwargs)
        super().__init__(*args, **defaults)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()

        if self.help_prefix:
            del kwargs['help_text']
            kwargs['help_prefix'] = self.help_prefix

        return (name, path, [self.config_name], kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': self.form_class}
        defaults.update(kwargs)
        return super().formfield(**defaults)

    @property
    def validators(self):
        default_validators = super().validators
        file_validators = [
            lambda file: validators.validate_file_type_and_size(
                file, self.file_config)
        ]
        file_validators.extend(default_validators)
        return file_validators

    @property
    def file_config(self):
        c = {}
        defaults = settings.FILE_ALIASES.get('*', {})
        c.update(defaults)

        if self.config_name:
            c.update(settings.FILE_ALIASES[self.config_name])
        return c

    @property
    def allowed_file_types(self):
        return ', '.join(name
                         for name, _
                         in self.file_config['fileformats'])

    @property
    def max_size_mb(self):
        return int(self.file_config['max_size']/(10**6))

    @property
    def _help_text(self):
        help_text = format_lazy(
            _(
                '{help_prefix} Allowed file formats are '
                '{allowed_file_types}. The file size should be max. '
                '{max_size_mb} MB.'
            ),
            help_prefix=self.help_prefix,
            max_size_mb=self.max_size_mb,
            allowed_file_types=self.allowed_file_types,
            **self.file_config
        )
        return help_text
