import factory
from django.db.models.signals import post_save
from django.utils.encoding import smart_str

from adhocracy4.test.helpers import redirect_target


@factory.django.mute_signals(post_save)
def setup_group_members(project, group_factory, user_factory):
    group_org = group_factory()
    project.organisation.groups.add(group_org)
    group_member_in_org = user_factory.create(groups=(group_org, ))

    group_pro = group_factory()
    project.group = group_pro
    project.save()
    group_member_in_pro = user_factory.create(groups=(group_pro, ))

    group_out = group_factory()
    group_member_out = user_factory.create(groups=(group_out, ))

    return project, group_member_in_org, group_member_in_pro, group_member_out


def assert_dashboard_form_component_response(
        response, component, status_code=200):
    assert response.status_code == status_code
    assert str(component.form_title) in smart_str(response.content)


def assert_dashboard_form_component_edited(
        response, component, obj, data, status_code=200):
    obj.refresh_from_db()
    assert redirect_target(response) == \
        'dashboard-{}-edit'.format(component.identifier)
    for key in data.keys():
        attr = getattr(obj, key)
        value = data.get(key)
        assert attr == value, '{} != {}'.format(attr, value)
