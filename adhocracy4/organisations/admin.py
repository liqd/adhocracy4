from django.contrib import admin

from . import models


class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(models.Organisation, OrganisationAdmin)
