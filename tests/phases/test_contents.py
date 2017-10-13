import pytest

from adhocracy4.phases import PhaseContent, content
from tests.apps.questions import models
from tests.apps.questions.phases import AskPhase


@pytest.fixture
def dummy_phase():
    class DummyPhase(PhaseContent):
        app = 'dummy'
        phase = 'phase'
        weight = 9999
        features = {
            'comment': (models.Question,)
        }

    return DummyPhase()


def test_registry_with_questions_app():
    assert 'a4test_questions:020:ask' in content
    assert content['a4test_questions:020:ask'].__class__ is AskPhase
    choice = ('a4test_questions:020:ask', 'AskPhase (a4test_questions:ask)')
    assert choice in content.as_choices()

    with pytest.raises(TypeError):
        content[12]


def test_phase_content(dummy_phase):
    assert dummy_phase.identifier == 'dummy:999:phase'
    assert str(dummy_phase) == 'DummyPhase (dummy:phase)'
    assert dummy_phase.has_feature('comment', models.Question)


def test_app_phases():
    assert (sorted(content.app_phases('a4test_questions'))
            == ['a4test_questions:020:ask', 'a4test_questions:030:rate'])
