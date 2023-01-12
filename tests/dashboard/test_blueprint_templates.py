import importlib

import pytest
from django.test.utils import override_settings

from adhocracy4.dashboard.blueprints import get_blueprints


@override_settings(A4_BLUEPRINT_TYPES=[("QS", "questions")])
@override_settings(
    A4_DASHBOARD={"BLUEPRINTS": "tests.project.blueprints_with_type.blueprints"}
)
@pytest.mark.django_db
def test_blueprint_template_with_types():
    # reload blueprints to reinitialize ProjectBlueprint with
    # overridden settings
    bp_module = importlib.import_module("adhocracy4.dashboard.blueprints")
    importlib.reload(bp_module)
    blueprints = get_blueprints()
    assert blueprints[0][1]._fields == (
        "title",
        "description",
        "content",
        "image",
        "settings_model",
        "type",
    )


@pytest.mark.django_db
def test_blueprint_template_without_types():
    bp_module = importlib.import_module("adhocracy4.dashboard.blueprints")
    importlib.reload(bp_module)
    blueprints = get_blueprints()
    assert blueprints[0][1]._fields == (
        "title",
        "description",
        "content",
        "image",
        "settings_model",
    )
