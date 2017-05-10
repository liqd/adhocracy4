from django.contrib import admin

from . import models


class FollowAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'creator', 'project', 'enabled')


admin.site.register(models.Follow, FollowAdmin)
