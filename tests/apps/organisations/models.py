from autoslug import AutoSlugField
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from adhocracy4.images import fields


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
