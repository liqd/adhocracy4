from django.contrib import admin

from . import models


class OrganisationAdmin(admin.ModelAdmin):
    raw_id_fields = ('initiators', )

admin.site.register(models.Organisation, OrganisationAdmin)
