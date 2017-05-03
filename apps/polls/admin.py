from django.contrib import admin

from . import models


class ChoiceInline(admin.TabularInline):
    model = models.Choice


class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        ChoiceInline
    ]


class VoteAdmin(admin.ModelAdmin):
    list_filter = ('choice__question',)


admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Vote, VoteAdmin)
