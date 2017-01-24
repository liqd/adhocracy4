from django.contrib import admin

from . import models


class OrganisationAdmin(admin.ModelAdmin):
    filter_horizontal = ('initiators',)


admin.site.register(models.Organisation, OrganisationAdmin)
