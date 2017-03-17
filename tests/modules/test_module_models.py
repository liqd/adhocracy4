import pytest

from tests.apps.questions import models as q_models


@pytest.mark.django_db
def test_has_feature(phase):
    module = phase.module
    assert module.has_feature('crud', q_models.Question)
