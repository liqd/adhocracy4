import pytest

from adhocracy4.modules import ModuleContent, content
from tests.apps.questions.phases import QuestionModule


@pytest.fixture
def dummy_module():
    class DummyModule(ModuleContent):
        app = 'dummy'
        name = 'DummyModule'
        description = 'Dummy module description'

    return DummyModule()


def test_phase_content(dummy_module):
    assert dummy_module.identifier == 'dummy:module'
    assert str(dummy_module) == 'DummyModule (dummy:module)'
    assert dummy_module.allowed_phases() == []


def test_registry_with_questions_app():
    assert 'a4test_questions:module' in content
    assert content['a4test_questions:module'].__class__ is QuestionModule
    choice = ('a4test_questions:module',
              'QuestionModule (a4test_questions:module)')
    assert choice in content.as_choices()

    assert 'a4test_questions:module' in content
    assert content['a4test_questions:module']
    assert 'a4test_questions' in content
    assert content['a4test_questions']

    assert '404:module' not in content
    with pytest.raises(KeyError):
        content['404:module']

    with pytest.raises(TypeError):
        12 in content
    with pytest.raises(TypeError):
        content[12]


def test_allowed_phases():
    module = content['a4test_questions:module']
    assert (sorted(module.allowed_phases())
            == ['a4test_questions:020:ask', 'a4test_questions:030:rate'])
