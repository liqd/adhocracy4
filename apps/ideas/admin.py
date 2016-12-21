from django.contrib import admin

from . import models


class IdeaAdmin(admin.ModelAdmin):
    list_filter = ('module__project', 'module')


admin.site.register(models.Idea, IdeaAdmin)
