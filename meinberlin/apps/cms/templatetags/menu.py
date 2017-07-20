from django import template

from meinberlin.apps.cms import models as cms_models

register = template.Library()


@register.assignment_tag
def get_menu(title):
    menu = cms_models.NavigationMenu.objects.filter(title=title).first()

    if menu is not None:
        return menu.items.all()
