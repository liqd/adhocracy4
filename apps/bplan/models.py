from django.contrib.auth.models import AnonymousUser
from django.db import models

from adhocracy4.models.base import TimeStampedModel
from adhocracy4.modules import models as module_models
from apps.extprojects.models import ExternalProject


class Bplan(ExternalProject):
    office_worker_email = models.EmailField()


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

    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    statement = models.TextField(max_length=17500)

    street_number = models.CharField(max_length=255)
    postal_code_city = models.CharField(max_length=255)
