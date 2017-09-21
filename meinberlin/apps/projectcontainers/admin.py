from django.contrib import admin

from meinberlin.apps.projectcontainers import models


@admin.register(models.ProjectContainer)
class ProjectContainerAdmin(admin.ModelAdmin):
    fields = ('name', 'organisation', 'description',
              'tile_image', 'tile_image_copyright',
              'is_draft', 'is_archived',
              'projects',
              )
