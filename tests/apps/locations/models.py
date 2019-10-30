from autoslug import AutoSlugField
from django.db import models

from adhocracy4.maps.fields import PointField
from adhocracy4.modules.models import Item


class Location(Item):
    slug = AutoSlugField(populate_from='name', unique=True)
    name = models.CharField(max_length=120)
    point = PointField()

    def get_absolute_url(self):
        return '/location/%s/' % self.pk
