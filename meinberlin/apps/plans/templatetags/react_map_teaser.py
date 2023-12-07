import json

from django import template
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from django.utils.html import format_html
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

from adhocracy4.administrative_districts.models import AdministrativeDistrict

register = template.Library()


@register.simple_tag(takes_context=False)
def react_map_teaser():
    city_wide = _("City wide")
    districts = AdministrativeDistrict.objects.all()
    district_names_list = [district.name for district in districts]
    district_names_list.append(str(city_wide))

    topics = getattr(settings, "A4_PROJECT_TOPICS", None)
    if topics:
        topics_enum = import_string(settings.A4_PROJECT_TOPICS)
        topic_dict = {i.name: str(i.label) for i in topics_enum}
    else:
        raise ImproperlyConfigured("set A4_PROJECT_TOPICS in settings")

    url = reverse("meinberlin_plans:plan-list")

    attributes = {
        "districtnames": district_names_list,
        "topicChoices": topic_dict,
        "url": url,
    }

    return format_html(
        '<div data-mb-widget="mapTeaser" ' 'data-attributes="{attributes}"></div>',
        attributes=json.dumps(attributes),
    )
