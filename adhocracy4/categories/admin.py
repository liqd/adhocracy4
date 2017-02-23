from django.contrib import admin

from . import models

class CategoryAdmin(admin.ModelAdmin):
    list_filter = ('module',)

admin.site.register(models.Category, CategoryAdmin)
