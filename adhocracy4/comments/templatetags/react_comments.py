import json

from django import template, utils
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe

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
    is_authenticated = user.is_authenticated()
    is_moderator = user.is_superuser or user in obj.project.moderators.all()
    user_name = user.username

    contenttype = ContentType.objects.get_for_model(obj)
    permission = '{ct.app_label}.comment_{ct.model}'.format(ct=contenttype)
    has_comment_permission = user.has_perm(permission, obj)

    comments_contenttype = ContentType.objects.get_for_model(Comment)
    pk = obj.pk

    language = utils.translation.get_language()

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
        'language': language,
        'isReadOnly': not has_comment_permission,
    }

    return mark_safe((
        '<div id={mountpoint}></div><script>window.opin.renderComment('
        '{mountpoint}, {attributes})</script>').format(
            attributes=json.dumps(attributes),
            mountpoint=json.dumps(mountpoint)
    )
    )
