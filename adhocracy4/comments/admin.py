from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    fields = (
        'content_type', 'content_object', 'comment', 'is_removed',
        'is_censored', 'is_moderator_marked', 'creator', 'comment_categories'
    )
    readonly_fields = ('creator', 'content_type', 'content_object')
    list_display = (
        '__str__', 'creator', 'is_removed', 'is_censored', 'created'
    )
    search_fields = ('comment',)
    date_hierarchy = 'created'
