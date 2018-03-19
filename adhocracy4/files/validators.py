import magic
import math

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

FILE_MAX_MB = 5


def validate_file_type_and_size(file, config):
    fileformats = config.get('fileformats')
    max_size = config.get('max_size', FILE_MAX_MB*10**6)
    names, mimetypes = zip(*fileformats)
    errors = []

    file.open()
    filetype = magic.from_buffer(file.read(1024), mime=True)
    if filetype.lower() not in mimetypes:
        msg = _(
            'Unsupported file format. Supported formats are {}.'.format(
                ', '.join(names)
            )
        )
        errors.append(ValidationError(msg))
    if file.size > max_size:
        max_size_mb = math.floor(max_size / 10 ** 6)
        msg = _('File should be at most {} MB'.format(max_size_mb))
        errors.append(ValidationError(msg))

    file.close()
    if errors:
        raise ValidationError(errors)
    return file
