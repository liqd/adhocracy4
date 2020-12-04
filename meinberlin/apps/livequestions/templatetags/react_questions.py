import json

from django import template
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from adhocracy4.rules.discovery import NormalUser

register = template.Library()


@register.simple_tag(takes_context=True)
def react_questions(context, obj):
    request = context['request']

    user = request.user
    is_moderator = \
        user.has_perm('meinberlin_livequestions.moderate_livequestions', obj)
    categories = [category.name for category in obj.category_set.all()]
    category_dict = {category.pk: category.name
                     for category in obj.category_set.all()}
    questions_api_url = reverse('questions-list', kwargs={'module_pk': obj.pk})
    private_policy_label = str(_('I hereby expressly consent to the storage '
                                 'and publication of my questions, as '
                                 'described in the {}privacy policy{}. I also '
                                 'confirm that I have read and accept the '
                                 '{}terms of use{} and the {}privacy '
                                 'policy{}.'))
    present_url = \
        reverse('meinberlin_livequestions:question-present',
                kwargs={'module_slug': obj.slug})
    like_permission = 'meinberlin_likes.add_like_model'
    has_liking_permission = user.has_perm(
        like_permission, obj)
    would_have_liking_permission = NormalUser().would_have_perm(
        like_permission, obj
    )

    ask_permissions = 'meinberlin_livequestions.add_livequestion'
    has_ask_questions_permissions = user.has_perm(ask_permissions, obj)
    would_have_ask_questions_permission = NormalUser().would_have_perm(
        ask_permissions, obj)

    attributes = {
        'information': obj.description,
        'questions_api_url': questions_api_url,
        'present_url': present_url,
        'isModerator': is_moderator,
        'categories': categories,
        'category_dict': category_dict,
        'hasLikingPermission': (has_liking_permission
                                or would_have_liking_permission),
        'hasAskQuestionsPermission': (has_ask_questions_permissions
                                      or would_have_ask_questions_permission),
        'privatePolicyLabel': private_policy_label,
    }

    return format_html(
        '<div data-ie-widget="questions" '
        'data-attributes="{attributes}"></div>',
        attributes=json.dumps(attributes)
    )


@register.simple_tag(takes_context=True)
def react_questions_present(context, obj):

    categories = [category.name for category in obj.category_set.all()]
    questions_api_url = reverse('questions-list', kwargs={'module_pk': obj.pk})
    request = context['request']
    url = obj.project.get_absolute_url()
    full_url = request.build_absolute_uri(url)

    attributes = {
        'questions_api_url': questions_api_url,
        'categories': categories,
        'url': full_url,
        'title': obj.project.name
    }

    return format_html(
        '<div data-ie-widget="present" '
        'data-attributes="{attributes}"></div>',
        attributes=json.dumps(attributes)
    )
