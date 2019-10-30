import pytest
from django import forms

from adhocracy4.categories.forms import CategorizableFieldMixin
from tests.apps.questions.models import Question


class CategoryForm(CategorizableFieldMixin, forms.ModelForm):

    class Meta:
        model = Question
        fields = ['category']


@pytest.mark.django_db
def test_choice(module, category_factory):
    category = category_factory(module=module)
    other_category = category_factory()
    form = CategoryForm(module=module)
    choice = form.fields['category'].queryset.all()
    assert category in choice
    assert other_category not in choice


@pytest.mark.django_db
def test_show_categories(module, category_factory):
    category_factory()
    form = CategoryForm(module=module)
    assert not form.show_categories()

    category_factory(module=module)
    form = CategoryForm(module=module)
    assert form.show_categories()
