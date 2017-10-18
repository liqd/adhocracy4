from django.contrib import admin

from . import models


class ChoiceInline(admin.TabularInline):
    model = models.Choice


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        ChoiceInline
    ]
    list_filter = (
        'poll__module__project__organisation', 'poll__module__project'
    )
    date_hierarchy = 'poll__created'
    search_fields = ('label',)
