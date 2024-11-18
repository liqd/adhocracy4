import sentry_sdk
from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from adhocracy4.administrative_districts.models import AdministrativeDistrict
from adhocracy4.models.base import TimeStampedModel
from adhocracy4.modules import models as module_models
from adhocracy4.projects.models import Topic
from meinberlin.apps.extprojects.models import ExternalProject


class Bplan(ExternalProject):
    identifier = models.CharField(
        verbose_name=_("Identifier"),
        help_text=_(
            "The identifier has to be identical to the identifier "
            "in the FIS-Broker, so that district and location are "
            "added automatically."
        ),
        blank=True,
        max_length=120,
    )
    is_diplan = models.BooleanField(default=False)
    office_worker_email = models.EmailField(
        verbose_name=_("Office worker email"),
        blank=True,
    )

    def save(self, update_fields=None, *args, **kwargs):
        if self.identifier:
            district = self._get_district_for_identifier()
            self.administrative_district = district
            if update_fields:
                update_fields = {"administrative_district"}.union(update_fields)
        super().save(update_fields, *args, **kwargs)
        topic = Topic.objects.get(code="URB")
        self.topics.add(topic)

    def _get_district_for_identifier(self):
        district_name = self._identifier_to_district()
        district = None
        if district_name:
            try:
                district = AdministrativeDistrict.objects.get(name=district_name)
            except AdministrativeDistrict.DoesNotExist as e:
                sentry_sdk.capture_exception(e)
        return district

    def _identifier_to_district(self):
        prefix = self.identifier.split("-")[0].strip()
        match prefix:
            case "1" | "I" | "II" | "III":
                return "Mitte"
            case "2" | "VI" | "V":
                return "Friedrichshain-Kreuzberg"
            case "3" | "IV" | "XVIII" | "XIX":
                return "Pankow"
            case "4" | "VII" | "IX":
                return "Charlottenburg-Wilmersdorf"
            case "5" | "VIII":
                return "Spandau"
            case "6" | "X" | "XII":
                return "Steglitz-Zehlendorf"
            case "7" | "XIII" | "XI":
                return "Tempelhof-Schöneberg"
            case "8" | "XIV":
                return "Neukölln"
            case "9" | "XV" | "XVI":
                return "Treptow-Köpenick"
            case "10" | "XXIII" | "XXI":
                return "Marzahn-Hellersdorf"
            case "11" | "XVII" | "XXII":
                return "Lichtenberg"
            case "12" | "XX":
                return "Reinickendorf"
            case _:
                return None


class AnonymousItem(TimeStampedModel):
    # TODO: remove this class once transition to diplan is complete
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
    # TODO: remove this class once transition to diplan is complete
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
