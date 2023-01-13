from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from adhocracy4.models.base import TimeStampedModel
from adhocracy4.modules import models as module_models
from meinberlin.apps.extprojects.models import ExternalProject


class Bplan(ExternalProject):
    identifier = models.CharField(
        verbose_name=_("Identifier"),
        help_text=_(
            "The identifier has to be identic to the identifier "
            "in the FIS-Broker, so that district and location are "
            "added automatically."
        ),
        blank=True,
        max_length=120,
    )
    office_worker_email = models.EmailField(
        verbose_name=_("Office worker email"),
        blank=True,
    )


class AnonymousItem(TimeStampedModel):
    module = models.ForeignKey(module_models.Module, on_delete=models.CASCADE)

    @property
    def project(self):
        return self.module.project

    @property
    def creator(self):
        return AnonymousUser()

    @creator.setter
    def creator(self, value):
        pass

    class Meta:
        abstract = True


class Statement(AnonymousItem):

    name = models.CharField(max_length=255, verbose_name=_("Your Name"))
    email = models.EmailField(blank=True, verbose_name=_("Email address"))
    statement = models.TextField(verbose_name=_("Statement"))

    street_number = models.CharField(
        max_length=255, verbose_name=_("Street, House number")
    )
    postal_code_city = models.CharField(
        max_length=255, verbose_name=_("Postal code, City")
    )

    class Meta:
        ordering = ["-created"]
