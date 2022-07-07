import importlib

import pytest
from django.conf import settings
from django.test.utils import override_settings
from django.utils.module_loading import import_string


@override_settings(A4_BLUEPRINT_TYPES=[('QS', 'questions')])
@pytest.mark.django_db
def test_blueprint_template_with_types_raises_error():
    # reload blueprints to reinitialize ProjectBlueprint with
    # overridden settings
    bp_module = importlib.import_module('adhocracy4.dashboard.blueprints')
    importlib.reload(bp_module)
    with pytest.raises(TypeError) as error:
        import_string(settings.A4_DASHBOARD['BLUEPRINTS'])
    assert str(error.value).\
        endswith('missing 1 required positional argument: \'type\'')


@pytest.mark.django_db
def test_blueprint_template_without_types():
    bp_module = importlib.import_module('adhocracy4.dashboard.blueprints')
    importlib.reload(bp_module)
    blueprints = import_string(settings.A4_DASHBOARD['BLUEPRINTS'])
    assert blueprints[0][1]._fields == ('title', 'description', 'content',
                                        'image', 'settings_model')
