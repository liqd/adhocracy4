from django.contrib import admin

from . import models

admin.site.register(models.AdministrativeDistrict, admin.ModelAdmin)
