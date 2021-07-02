import os

import factory
from django.conf import settings
from django.db.models.signals import post_save
from django.utils.encoding import smart_text
from easy_thumbnails.files import get_thumbnailer

from adhocracy4.test.helpers import redirect_target


@factory.django.mute_signals(post_save)
def setup_group_member(organisation, project, group_factory,
                       user_factory):
    group1 = group_factory()
    group_member = user_factory.create(groups=(group1, ))
    if organisation:
        organisation.groups.add(group1)
    else:
        organisation = None
    if project:
        organisation = project.organisation
        organisation.groups.add(group1)
        project.group = group1
        project.save()
    else:
        project = None
    return group_member, organisation, project


def assert_template_response(response, template_name, status_code=200):
    assert response.status_code == status_code
    response_template = response.template_name[0]
    assert response_template == template_name, \
        '{} != {}'.format(response_template, template_name)


def assert_dashboard_form_component_response(
        response, component, status_code=200):
    assert response.status_code == status_code
    assert str(component.form_title) in smart_text(response.content)


def assert_dashboard_form_component_edited(
        response, component, obj, data, status_code=200):
    obj.refresh_from_db()
    assert redirect_target(response) == \
        'dashboard-{}-edit'.format(component.identifier)
    for key in data.keys():
        attr = getattr(obj, key)
        value = data.get(key)
        assert attr == value, '{} != {}'.format(attr, value)


def createThumbnail(imagefield):
    thumbnailer = get_thumbnailer(imagefield)
    thumbnail = thumbnailer.generate_thumbnail(
        {'size': (800, 400), 'crop': 'smart'})
    thumbnailer.save_thumbnail(thumbnail)
    thumbnail_path = os.path.join(settings.MEDIA_ROOT, thumbnail.path)
    return thumbnail_path
