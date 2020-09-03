from django.contrib import admin

from . import models


class LiveQuestionAdmin(admin.ModelAdmin):
    list_filter = ('module__project', 'module')


admin.site.register(models.LiveQuestion, LiveQuestionAdmin)
