from autoslug import AutoSlugField
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from adhocracy4.images import fields


class Organisation(models.Model):
    slug = AutoSlugField(populate_from='name', unique=True)
    name = models.CharField(max_length=512)
    initiators = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
    )
    logo = fields.ConfiguredImageField(
        'logo',
        verbose_name=_('Logo'),
        help_prefix=_(
            'The image will be shown in the newsletter in the banner.'
        ),
        upload_to='projects/backgrounds',
        blank=True)

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
