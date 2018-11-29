from django.db import models
from wagtail.wagtailimages.models import AbstractImage
from wagtail.wagtailimages.models import AbstractRendition
from wagtail.wagtailimages.models import Image


class CustomImage(AbstractImage):

    copyright = models.CharField(max_length=255, blank=True)

    admin_form_fields = Image.admin_form_fields + (
        'copyright',
    )


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(CustomImage, related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )
