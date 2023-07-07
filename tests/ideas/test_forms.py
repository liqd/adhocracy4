import pytest
from django.utils.translation import gettext_lazy as _

from meinberlin.apps.ideas.forms import IdeaForm


@pytest.mark.django_db
def test_idea_form_with_mixins(module, category_alias_factory, label_alias_factory):
    form = IdeaForm(module=module)
    fields = ["name", "description", "image", "category", "labels", "right_of_use"]

    for field in fields:
        assert field in form.fields

    assert form.fields["category"].label == _("Category")
    assert form.fields["labels"].label == _("Labels")

    category_alias = category_alias_factory(module=module)
    label_alias = label_alias_factory(module=module)
    form = IdeaForm(module=module)

    assert form.fields["category"].label == category_alias.title
    assert form.fields["labels"].label == label_alias.title
