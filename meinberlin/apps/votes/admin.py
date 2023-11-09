from django.contrib import admin

from .models import TokenPackage
from .models import TokenVote
from .models import VotingToken


@admin.register(VotingToken)
class VotingTokenAdmin(admin.ModelAdmin):
    fields = (
        "token",
        "token_hash",
        "module",
        "is_active",
        "package",
        "allowed_votes",
    )
    readonly_fields = ("token", "token_hash", "package")
    list_display = ("pk", "__str__", "project", "module", "module_name", "is_active")
    list_filter = ("module__project",)

    def delete_model(self, request, obj):
        obj.package.size -= 1
        obj.package.save()
        super().delete_model(request, obj)

    @admin.display(description="Module Name")
    def module_name(self, token):
        return token.module.name

    def save_model(self, request, obj, form, change):
        if not hasattr(obj, "package"):
            obj.package = TokenPackage.objects.create(module=obj.module, size=1)

        if not obj.token_hash:
            obj.token_hash = VotingToken.hash_token(obj.token, obj.module)
        super().save_model(request, obj, form, change)


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

    @admin.display(description="Module")
    def token_module(self, token_vote):
        return token_vote.token.module.name

    @admin.display(description="Project")
    def token_project(self, token_vote):
        return token_vote.token.project
