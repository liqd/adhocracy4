from django.contrib import admin

from .models import TokenVote
from .models import VotingToken


@admin.register(VotingToken)
class VotingTokenAdmin(admin.ModelAdmin):
    fields = (
        "token",
        "token_hash",
        "module",
        "is_active",
        "package_number",
        "allowed_votes",
    )
    readonly_fields = ("token", "token_hash", "package_number")
    list_display = ("pk", "__str__", "project", "module", "module_name", "is_active")
    list_filter = ("module__project",)

    def module_name(self, token):
        return token.module.name

    def save_model(self, request, obj, form, change):
        if obj.package_number is None:
            obj.package_number = VotingToken.next_package_number(obj.module)
        if not obj.token_hash:
            obj.token_hash = VotingToken.hash_token(obj.token, obj.module)
        super().save_model(request, obj, form, change)

    module_name.short_description = "Module Name"


@admin.register(TokenVote)
class TokenVoteAdmin(admin.ModelAdmin):
    fields = ("token_hash", "content_type", "content_object")
    readonly_fields = ("token_hash", "content_type", "content_object")
    list_display = ("content_object", "token_project", "token_module", "created")
    list_filter = (
        "token__module",
        "token__module__project",
    )
    date_hierarchy = "created"

    def token_hash(self, token_vote):
        return token_vote.token.token_hash

    def token_module(self, token_vote):
        return token_vote.token.module.name

    def token_project(self, token_vote):
        return token_vote.token.project

    token_module.short_description = "Module"
    token_project.short_description = "Project"
