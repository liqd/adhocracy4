import pytest

from adhocracy4.dashboard.components import DashboardComponent
from adhocracy4.dashboard.components import DashboardComponents


def test_register(dashboard_test_component_factory):
    project_component0 = dashboard_test_component_factory(
        weight=0, identifier='b')
    project_component1 = dashboard_test_component_factory(
        weight=0, identifier='a')
    module_component = dashboard_test_component_factory(identifier='c')

    components = DashboardComponents()
    components.register_project(project_component0)
    components.register_project(project_component1)
    components.register_module(module_component)

    assert components.projects == {'b': project_component0,
                                   'a': project_component1}
    assert components.modules == {'c': module_component}

    assert components.get_project_components() == [project_component1,
                                                   project_component0]
    assert components.get_module_components() == [module_component]


def test_register_unique_id(dashboard_test_component):
    components = DashboardComponents()

    components.register_project(dashboard_test_component)
    with pytest.raises(ValueError):
        components.register_project(dashboard_test_component)

    components.register_module(dashboard_test_component)
    with pytest.raises(ValueError):
        components.register_module(dashboard_test_component)


def test_replace(dashboard_test_component_factory):
    components = DashboardComponents()

    component0 = dashboard_test_component_factory(
        identifier='test', label='original')
    component1 = dashboard_test_component_factory(
        identifier='test', label='overwrite')
    component2 = dashboard_test_component_factory(
        identifier='test', label='overwrite-immediately')

    components.register_module(component0)
    components.replace_module(component1)
    assert components.modules['test'] == component0

    components.register_project(component0)
    components.replace_project(component1)
    assert components.projects['test'] == component0

    components.apply_replacements()

    assert components.modules['test'] == component1
    assert components.projects['test'] == component1

    components.replace_module(component2)
    assert components.modules['test'] == component2

    components.replace_project(component2)
    assert components.projects['test'] == component2


def test_urls(dashboard_test_component_factory):
    def fake_view(**args):
        pass

    project_component = dashboard_test_component_factory(
        urls=[('^pc-url-pattern$', fake_view, 'pc-url')])
    module_component = dashboard_test_component_factory(
        urls=[('^mc-url-pattern$', fake_view, 'mc-url')])

    components = DashboardComponents()
    components.register_project(project_component)
    components.register_module(module_component)

    urlpatterns = components.get_urls()
    assert len(urlpatterns) == 2

    assert any(map(lambda urlpattern: urlpattern.resolve('pc-url-pattern'),
                   urlpatterns))
    assert any(map(lambda urlpattern: urlpattern.resolve('mc-url-pattern'),
                   urlpatterns))


def test_component_interface():
    component = DashboardComponent()
    assert component.is_effective(None) is False
    assert component.get_progress(None) == (0, 0)
    assert component.get_urls() == []
    assert component.get_base_url(None) == ''
