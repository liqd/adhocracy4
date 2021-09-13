import pytest
from django.urls import reverse
from django.utils.translation import ngettext

from adhocracy4.test.helpers import assert_template_response
from meinberlin.apps.users.models import User


@pytest.mark.django_db
def test_user_admin_form(client,
                         organisation_factory,
                         user_factory,
                         group_factory):

    admin = user_factory(is_superuser=True, is_staff=True)
    group1 = group_factory()
    group2 = group_factory()

    user = user_factory()

    organisation = organisation_factory(groups=(group1, group2))

    client.force_login(admin)

    url = reverse(
        'admin:meinberlin_users_user_change',
        args=(user.id,))

    response = client.get(url)
    assert_template_response(
        response,
        'admin/meinberlin_users/user/change_form.html')

    data = {'username': user.username,
            'email': user.email,
            'groups': group1.id}

    response = client.post(url, data)

    assert response.status_code == 302
    user = User.objects.get(username=user.username)
    assert user.groups.all().count() == 1
    assert user.groups.all().first() == group1

    data = {'username': user.username,
            'email': user.email,
            'groups': [group1.id, group2.id]
            }
    response = client.post(url, data)

    msg = ngettext('User is member in more than one group in this '
                   'organisation: %(duplicates)s.', '',
                   1) % {'duplicates': organisation.name}

    assert msg in response.context['errors'][0]
    assert_template_response(
        response, 'admin/meinberlin_users/user/change_form.html')

    group1.organisation_set.remove(organisation)

    response = client.post(url, data)
    assert response.status_code == 302
