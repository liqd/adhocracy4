from autoslug import AutoSlugField
from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from adhocracy4.images import fields


class Organisation(models.Model):
    slug = AutoSlugField(populate_from="name", unique=True, editable=True)
    name = models.CharField(max_length=512)
    initiators = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
    )
    groups = models.ManyToManyField(Group, blank=True)
    logo = fields.ConfiguredImageField(
        "logo",
        verbose_name=_("Logo"),
        help_prefix=_(
            "The image will be shown in the newsletter in the banner, "
            "as such it should not be wider than 650 pixels."
        ),
        upload_to="organisation/logos",
        blank=True,
    )
    address = models.TextField(blank=True, verbose_name=_("Postal address"))
    url = models.URLField(blank=True, verbose_name=_("Website of organisation"))

    def __str__(self):
        return self.name

    def has_initiator(self, user):
        return user in self.initiators.all()

    def get_absolute_url(self):
        return reverse("meinberlin_plans:plan-list")
