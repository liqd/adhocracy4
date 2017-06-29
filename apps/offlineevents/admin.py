from django.contrib import admin

from . import models

admin.site.register(models.OfflineEvent, admin.ModelAdmin)
