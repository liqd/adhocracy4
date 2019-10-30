from autoslug import AutoSlugField
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Organisation(models.Model):
    name = models.CharField(max_length=512)
    slug = AutoSlugField(populate_from='name', unique=True)
    initiators = models.ManyToManyField(
        User,
        blank=True,
    )
    groups = models.ManyToManyField(
        Group,
        blank=True
    )

    def __str__(self):
        return self.name

    def has_initiator(self, user):
        return user in self.initiators.all()

    def get_absolute_url(self):
        from django.utils.http import urlencode
        return '%s?%s' % (
            reverse('project-list'),
            urlencode({'organisation': self.pk})
        )
