from unittest import mock

import pytest

from adhocracy4.dashboard import ProjectDashboard


@pytest.mark.django_db
def test_progress(module, dashboard_test_component_factory):
    project_components = [dashboard_test_component_factory(progress=(2, 3))]
    module_components = [dashboard_test_component_factory(progress=(1, 1))]

    project = module.project
    project_dashboard = ProjectDashboard(project)
    project_dashboard.get_project_components = \
        mock.MagicMock(return_value=project_components)
    project_dashboard.get_module_components = \
        mock.MagicMock(return_value=module_components)

    assert project_dashboard.get_progress() == (3, 4)


@pytest.mark.django_db
def test_menu(module, dashboard_test_component_factory):
    project_components = [dashboard_test_component_factory(urls=['pc1_url'])]
    module_components = [dashboard_test_component_factory(urls=['mc1_url'])]

    project = module.project
    project_dashboard = ProjectDashboard(project)
    project_dashboard.get_project_components = \
        mock.MagicMock(return_value=project_components)
    project_dashboard.get_module_components = \
        mock.MagicMock(return_value=module_components)

    project_component = project_components[0]
    assert project_dashboard.get_project_menu(project_component) == [
        {
            'label': project_component.label,
            'is_active': True,
            'url': 'pc1_url',
            'is_complete': True
        }
    ]

    module_component = module_components[0]
    assert project_dashboard.get_module_menu(
        module, module, module_component) == [
        {
            'label': module_component.label,
            'is_active': True,
            'url': 'mc1_url',
            'is_complete': True
        }
    ]

    assert project_dashboard.get_menu(None, project_component) == {
        'project': [{
            'label': project_component.label,
            'is_active': True,
            'url': 'pc1_url',
            'is_complete': True
        }],
        'modules': [{
            'module': module,
            'menu': [{
                'label': module_component.label,
                'is_active': False,
                'url': 'mc1_url',
                'is_complete': True
            }],
            'is_complete': True,
        }]
    }
