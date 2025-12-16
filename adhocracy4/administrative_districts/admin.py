from django.contrib import admin

from . import models


@admin.register(models.AdministrativeDistrict)
class AdministrativeDistrictAdmin(admin.ModelAdmin):
    list_display = ["name", "short_code"]
    fields = ["name", "short_code"]
    ordering = ["name"]
