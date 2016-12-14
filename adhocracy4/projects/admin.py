from django.contrib import admin

from . import models


class ProjectAdmin(admin.ModelAdmin):
    filter_horizontal = ('moderators', 'participants')


admin.site.register(models.Project, ProjectAdmin)
