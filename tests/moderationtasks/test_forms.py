import pytest
from django.utils.translation import gettext_lazy as _

from meinberlin.apps.moderationtasks.forms import ModerationTaskForm


@pytest.mark.django_db
def test_moderation_task_form(module):
    form = ModerationTaskForm(module=module)
    assert 'name' in form.fields
    assert form.fields['name'].label == _('Moderation task')
