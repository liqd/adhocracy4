import json

from django import template
from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html

from adhocracy4.modules.predicates import is_context_member
from adhocracy4.rules.discovery import NormalUser

from ..models import Comment
from ..serializers import ThreadSerializer

register = template.Library()


@register.simple_tag(takes_context=True)
def react_comments(context, obj):
    request = context['request']

    serializer = ThreadSerializer(
        obj.comments.all().order_by('-created'),
        many=True, context={'request': request})
    comments = serializer.data

    user = request.user
    is_authenticated = bool(user.is_authenticated)
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
        'isContextMember': (is_context_member(user, obj)
                            or is_context_member(NormalUser(), obj))
    }

    return format_html(
        '<div data-a4-widget="comment" data-attributes="{attributes}"></div>',
        attributes=json.dumps(attributes)
    )
