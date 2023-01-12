import pytest
from django import forms

from adhocracy4.labels.mixins import LabelsAddableFieldMixin
from tests.apps.ideas.models import Idea


class LabelForm(LabelsAddableFieldMixin, forms.ModelForm):
    class Meta:
        model = Idea
        fields = ["labels"]


@pytest.mark.django_db
def test_choice(module, label_factory):
    label1 = label_factory(module=module)
    label2 = label_factory()
    form = LabelForm(module=module)
    choice = form.fields["labels"].queryset.all()
    assert label1 in choice
    assert label2 not in choice


@pytest.mark.django_db
def test_show_labels(module, label_factory):
    label_factory()
    form = LabelForm(module=module)
    assert not form.show_labels()

    label_factory(module=module)
    form = LabelForm(module=module)
    assert form.show_labels()
