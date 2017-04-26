from django.contrib import admin

from . import models


class ChoiceInline(admin.TabularInline):
    model = models.Choice


class PollAdmin(admin.ModelAdmin):
    inlines = [
        ChoiceInline
    ]


class VoteAdmin(admin.ModelAdmin):
    list_filter = ('choice__poll',)


admin.site.register(models.Poll, PollAdmin)
admin.site.register(models.Vote, VoteAdmin)
