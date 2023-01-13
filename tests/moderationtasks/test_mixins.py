import pytest
from django import forms

from meinberlin.apps.budgeting.models import Proposal
from meinberlin.apps.moderationtasks.mixins import TasksAddableFieldMixin


class TaskForm(TasksAddableFieldMixin, forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ["completed_tasks"]


@pytest.mark.django_db
def test_choice(module, moderation_task_factory, proposal_factory):
    task1 = moderation_task_factory(module=module)
    task2 = moderation_task_factory()
    proposal = proposal_factory(module=module)

    form = TaskForm(instance=proposal)
    choice = form.fields["completed_tasks"].queryset.all()
    assert task1 in choice
    assert task2 not in choice


@pytest.mark.django_db
def test_show_labels(module, moderation_task_factory, proposal_factory):
    proposal = proposal_factory(module=module)
    moderation_task_factory()
    form = TaskForm(instance=proposal)
    assert not form.show_tasks()

    moderation_task_factory(module=module)
    form = TaskForm(instance=proposal)
    assert form.show_tasks()
