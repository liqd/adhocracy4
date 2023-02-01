from django.contrib import admin

from .models import TokenVote
from .models import VotingToken


@admin.register(VotingToken)
class VotingTokenAdmin(admin.ModelAdmin):
    fields = ("token", "module", "is_active", "allowed_votes")
    readonly_fields = ("token",)
    list_display = ("__str__", "project", "module", "module_name", "is_active")
    list_filter = ("module__project",)

    def module_name(self, token):
        return token.module.name

    module_name.short_description = "Module Name"


@admin.register(TokenVote)
class TokenVoteAdmin(admin.ModelAdmin):
    fields = ("token", "content_type", "content_object")
    readonly_fields = ("token", "content_type", "content_object")
    list_display = ("content_object", "token_project", "token_module", "created")
    list_filter = (
        "token__module",
        "token__module__project",
    )
    date_hierarchy = "created"

    def token_module(self, token_vote):
        return token_vote.token.module.name

    def token_project(self, token_vote):
        return token_vote.token.project

    token_module.short_description = "Module"
    token_project.short_description = "Project"
