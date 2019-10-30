from io import BytesIO

from django.core.files import base
from django.core.files import images
from PIL import Image


class ImageFactory():
    """
    Create a django file object containg an image.
    """

    def __call__(self, resolution, image_format='JPEG', name=None):

        filename = name or 'default.{}'.format(image_format.lower())
        color = 'blue'
        image = Image.new('RGB', resolution, color)
        image_data = BytesIO()
        image.save(image_data, image_format)
        image_content = base.ContentFile(image_data.getvalue())
        return images.ImageFile(image_content.file, filename)
