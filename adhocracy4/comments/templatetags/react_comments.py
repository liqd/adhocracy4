import json

from django import template
from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html

from ..models import Comment
from ..serializers import ThreadSerializer
from adhocracy4.rules.discovery import NormalUser

register = template.Library()


@register.simple_tag(takes_context=True)
def react_comments(context, obj):
    request = context['request']

    serializer = ThreadSerializer(
        obj.comments.all().order_by('-created'),
        many=True, context={'request': request})
    comments = serializer.data

    user = request.user
    is_authenticated = user.is_authenticated()
    is_moderator = user.is_superuser or user in obj.project.moderators.all()
    user_name = user.username

    contenttype = ContentType.objects.get_for_model(obj)
    permission = '{ct.app_label}.comment_{ct.model}'.format(ct=contenttype)
    has_comment_permission = user.has_perm(permission, obj)

    would_have_comment_permission = NormalUser().would_have_perm(
        permission, obj
    )

    comments_contenttype = ContentType.objects.get_for_model(Comment)
    pk = obj.pk

    mountpoint = 'comments_for_{contenttype}_{pk}'.format(
        contenttype=contenttype.pk,
        pk=pk
    )
    attributes = {
        'comments': comments,
        'comments_contenttype': comments_contenttype.pk,
        'subjectType': contenttype.pk,
        'subjectId': pk,
        'isAuthenticated': is_authenticated,
        'isModerator': is_moderator,
        'user_name': user_name,
        'isReadOnly': (not has_comment_permission and
                       not would_have_comment_permission),
    }

    return format_html(
        (
            '<div id="{mountpoint}" data-attributes="{attributes}"></div>'
            "<script>window.adhocracy4.renderComment('{mountpoint}')</script>"
        ),
        attributes=json.dumps(attributes),
        mountpoint=mountpoint
    )
