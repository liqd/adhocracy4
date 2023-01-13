from django.contrib import admin

from . import forms
from . import models


class OrganisationAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    raw_id_fields = ("initiators",)
    form = forms.OrganisationForm


admin.site.register(models.Organisation, OrganisationAdmin)
