from django.contrib import admin

from . import models


@admin.register(models.Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'creator', 'project', 'enabled')
    readonly_fields = ('creator',)
