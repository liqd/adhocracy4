from django.contrib import admin

from meinberlin.apps.ideas.admin import IdeaAdmin

from . import models

admin.site.register(models.Proposal, IdeaAdmin)
