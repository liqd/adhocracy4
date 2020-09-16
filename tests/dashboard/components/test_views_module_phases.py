import pytest

from adhocracy4.dashboard import components
from adhocracy4.test.helpers import redirect_target

component = components.modules.get('phases')


@pytest.mark.django_db
def test_edit_view(client, project, module_factory,
                   phase_factory, admin):
    module = module_factory(project=project)
    phase_0 = phase_factory(module=module)
    phase_1 = phase_factory(module=module)
    url = component.get_base_url(module)
    client.login(username=admin.username, password='password')
    response = client.get(url)
    assert response.status_code == 200

    data = {
        'phase_set-TOTAL_FORMS': '2',
        'phase_set-INITIAL_FORMS': '2',
        'phase_set-MIN_NUM_FORMS': '0',
        'phase_set-MAX_NUM_FORMS': '1000',

        'phase_set-0-name': 'Name 0',
        'phase_set-0-description': 'some description for phase 0',
        'phase_set-0-start_date_0': '2020-09-17',
        'phase_set-0-start_date_1': '19:23',
        'phase_set-0-end_date_0': '2020-10-23',
        'phase_set-0-end_date_1': '16:12',
        'phase_set-0-type': phase_0.type,
        'phase_set-0-id': phase_0.id,

        'phase_set-1-name': 'Name 1',
        'phase_set-1-description': 'some description for phase 1',
        'phase_set-1-start_date_0': '2020-10-24',
        'phase_set-1-start_date_1': '19:23',
        'phase_set-1-end_date_0': '2020-10-30',
        'phase_set-1-end_date_1': '16:12',
        'phase_set-1-type': phase_1.type,
        'phase_set-1-id': phase_1.id,
    }
    response = client.post(url, data)
    assert redirect_target(response) == 'dashboard-phases-edit'
    module.refresh_from_db()
    assert module.phase_set.get(id=phase_0.id).name \
        == data.get('phase_set-0-name')
    assert module.phase_set.get(id=phase_0.id).description \
        == data.get('phase_set-0-description')
    assert module.phase_set.get(id=phase_1.id).name \
        == data.get('phase_set-1-name')
    assert module.phase_set.get(id=phase_1.id).description \
        == data.get('phase_set-1-description')


@pytest.mark.django_db
def test_edit_view_validation(client, project, module_factory,
                              phase_factory, admin):
    module = module_factory(project=project)
    phase_0 = phase_factory(module=module)
    phase_1 = phase_factory(module=module)
    url = component.get_base_url(module)
    client.login(username=admin.username, password='password')
    response = client.get(url)
    assert response.status_code == 200

    data = {
        'phase_set-TOTAL_FORMS': '2',
        'phase_set-INITIAL_FORMS': '2',
        'phase_set-MIN_NUM_FORMS': '0',
        'phase_set-MAX_NUM_FORMS': '1000',

        'phase_set-0-name': 'Name 0',
        'phase_set-0-description': 'some description for phase 0',
        'phase_set-0-start_date_0': '2020-09-17',
        'phase_set-0-start_date_1': '19:23',
        'phase_set-0-end_date_0': '2020-10-23',
        'phase_set-0-end_date_1': '16:12',
        'phase_set-0-type': phase_0.type,
        'phase_set-0-id': phase_0.id,

        'phase_set-1-name': 'Name 1',
        'phase_set-1-description': 'some description for phase 1',
        'phase_set-1-start_date_0': '2020-10-22',
        'phase_set-1-start_date_1': '19:23',
        'phase_set-1-end_date_0': '2020-10-30',
        'phase_set-1-end_date_1': '16:12',
        'phase_set-1-type': phase_1.type,
        'phase_set-1-id': phase_1.id,
    }

    response = client.post(url, data)
    errors = response.context_data['form'].errors
    assert ({'end_date':
            ['Phases cannot run at the same time and must follow '
             'after each other.']}
            in errors)


@pytest.mark.django_db
def test_edit_view_validation_2(client, project, module_factory,
                                phase_factory, admin):
    module = module_factory(project=project)
    phase_0 = phase_factory(module=module)
    phase_1 = phase_factory(module=module)
    url = component.get_base_url(module)
    client.login(username=admin.username, password='password')
    response = client.get(url)
    assert response.status_code == 200

    data = {
        'phase_set-TOTAL_FORMS': '2',
        'phase_set-INITIAL_FORMS': '2',
        'phase_set-MIN_NUM_FORMS': '0',
        'phase_set-MAX_NUM_FORMS': '1000',

        'phase_set-0-name': 'Name 0',
        'phase_set-0-description': 'some description for phase 0',
        'phase_set-0-start_date_0': '2020-10-23',
        'phase_set-0-start_date_1': '19:23',
        'phase_set-0-end_date_0': '2020-09-17',
        'phase_set-0-end_date_1': '16:12',
        'phase_set-0-type': phase_0.type,
        'phase_set-0-id': phase_0.id,

        'phase_set-1-name': 'Name 1',
        'phase_set-1-description': 'some description for phase 1',
        'phase_set-1-start_date_0': '2020-10-22',
        'phase_set-1-start_date_1': '19:23',
        'phase_set-1-end_date_0': '2020-10-30',
        'phase_set-1-end_date_1': '16:12',
        'phase_set-1-type': phase_1.type,
        'phase_set-1-id': phase_1.id,
    }

    response = client.post(url, data)
    errors = response.context_data['form'].errors
    assert ({'end_date':
            ['End date can not be before start date.']}
            in errors)
