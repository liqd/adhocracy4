import json

from django import template
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from django.utils.html import format_html

from adhocracy4.comments.models import Comment
from adhocracy4.modules.predicates import is_context_member
from adhocracy4.rules.discovery import NormalUser

register = template.Library()


@register.simple_tag(takes_context=True)
def react_comments_async(context, obj, with_categories=False):
    request = context['request']
    user = request.user
    is_authenticated = bool(user.is_authenticated)
    is_moderator = user.is_superuser or user in obj.project.moderators.all()
    user_name = str(user.id)

    anchoredCommentId = request.GET.get('comment', '')

    contenttype = ContentType.objects.get_for_model(obj)
    permission = '{ct.app_label}.comment_{ct.model}'.format(ct=contenttype)
    has_comment_permission = user.has_perm(permission, obj)

    would_have_comment_permission = NormalUser().would_have_perm(
        permission, obj)

    comments_contenttype = ContentType.objects.get_for_model(Comment)
    pk = obj.pk

    comments_api_url = reverse('comments-list',
                               kwargs={'content_type': contenttype.pk,
                                       'object_pk': obj.pk}
                               )

    with_categories = bool(with_categories)

    comment_category_choices = {}
    if with_categories:
        comment_category_choices = getattr(settings,
                                           'A4_COMMENT_CATEGORIES', None)
        if comment_category_choices:
            comment_category_choices = dict(
                (x, str(y)) for x, y in comment_category_choices)
        else:
            raise ImproperlyConfigured('set A4_COMMENT_CATEGORIES in settings')

    '''
    isReadOnly - true if phase does not allow comment or project is non-public
                 and user is not participant or project is draft
                 (negation of modules.predicates.is_allowed_comment_item)
    isContextMember - true if project is public or user is
                      participant/moderator/org_member
    '''
    attributes = {
        'commentsApiUrl': comments_api_url,
        'comments_contenttype': comments_contenttype.pk,
        'subjectType': contenttype.pk,
        'subjectId': pk,
        'isAuthenticated': is_authenticated,
        'isModerator': is_moderator,
        'user_name': user_name,
        'isReadOnly': (not has_comment_permission
                       and not would_have_comment_permission),
        'commentCategoryChoices': comment_category_choices,
        'anchoredCommentId': anchoredCommentId,
        'withCategories': with_categories,
        'isContextMember': (is_context_member(user, obj)
                            or is_context_member(NormalUser(), obj))
    }

    return format_html(
        '<div data-a4-widget="comment_async" '
        'data-attributes="{attributes}"></div>',
        attributes=json.dumps(attributes))
