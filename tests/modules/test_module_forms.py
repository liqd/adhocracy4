import pytest
from tests.apps.questions import views as q_views


@pytest.mark.django_db
def test_item_create_form(rf, phase):
    module = phase.module
    settings_instance = \
        getattr(module, 'settings_instance', None)

    view = q_views.QuestionCreateForm()
    view.request = rf.get('/create/module/question/')
    view.module = module

    form = view.get_form()

    assert form.module == module
    assert form.settings_instance == settings_instance


@pytest.mark.django_db
def test_item_update_form(rf, question):
    object = question
    module = object.module
    settings_instance = \
        getattr(module, 'settings_instance', None)

    view = q_views.QuestionUpdateForm()
    view.request = rf.get('/1/update/')
    view.object = question

    form = view.get_form()

    assert form.module == module
    assert form.settings_instance == settings_instance
