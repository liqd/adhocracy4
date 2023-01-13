from allauth.account import urls as account_urls
from django import template
from django.urls import Resolver404
from django.urls import resolve

INVALID_URL_NAME = object()

register = template.Library()


def _is_account_url(request):
    try:
        url_name = resolve(request.path).url_name
    except Resolver404:
        return False

    return any(url_name == url.name for url in account_urls.urlpatterns)


def get_next_url(request):
    if _is_account_url(request):
        return request.GET.get("next") or request.POST.get("next") or "/"
    else:
        return request.get_full_path()


@register.inclusion_tag("meinberlin_users/indicator.html", takes_context=True)
def userindicator(context):
    if hasattr(context, "request"):
        context["redirect_field_value"] = get_next_url(context["request"])
    return context
