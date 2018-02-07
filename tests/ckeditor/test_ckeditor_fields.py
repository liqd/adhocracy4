import pytest


@pytest.mark.django_db
def test_ckeditor_collapsible_field(project):
    ckeditor_field = project._meta.get_field('information')
    assert 'collapsibleItem' in ckeditor_field.extra_plugins
    assert ('collapsibleItem', '/static/ckeditor_collapsible/', 'plugin.js') \
        in ckeditor_field.external_plugin_resources
