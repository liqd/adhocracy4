import json

from django import template
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.utils.html import format_html

from adhocracy4.modules.predicates import is_context_member
from adhocracy4.rules.discovery import NormalUser

register = template.Library()


@register.simple_tag(takes_context=True)
def react_comments_async(context, obj, with_categories=False):
    request = context['request']
    user = request.user

    anchoredCommentId = request.GET.get('comment', '')

    contenttype = ContentType.objects.get_for_model(obj)
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
    isContextMember - true if project is public or user is
                      participant/moderator/org_member
    '''
    attributes = {
        'subjectType': contenttype.pk,
        'subjectId': obj.pk,
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
