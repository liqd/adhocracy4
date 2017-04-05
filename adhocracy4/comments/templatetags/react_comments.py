import json

from django import template
from django.contrib.contenttypes.models import ContentType

from ..models import Comment
from ..serializers import ThreadSerializer

register = template.Library()


@register.inclusion_tag('a4comments/react_comments.html', takes_context=True)
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
        'isReadOnly': not has_comment_permission,
    }

    context = {
        'attributes': json.dumps(attributes),
        'mountpoint': mountpoint
    }

    return context
