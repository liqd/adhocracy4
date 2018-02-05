from autoslug import AutoSlugField
from django.db import models


class Organisation(models.Model):
    name = models.CharField(max_length=512, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True)

    class Meta:
        swappable = 'A4_ORGANISATIONS_MODEL'

    def __str__(self):
        return self.name

    def has_initiator(self, user):
        return user.is_staff
