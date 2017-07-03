from django.contrib import admin

from . import models


class ChoiceInline(admin.TabularInline):
    model = models.Choice


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        ChoiceInline
    ]
