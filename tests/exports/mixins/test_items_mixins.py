import pytest

from adhocracy4.exports.mixins import ItemExportWithCategoriesMixin
from adhocracy4.exports.mixins import ItemExportWithLabelsMixin
from adhocracy4.exports.mixins import ItemExportWithModeratorFeedback
from adhocracy4.exports.mixins import ItemExportWithReferenceNumberMixin


@pytest.mark.django_db
def test_item_categories_mixin(idea_factory, category):
    idea = idea_factory(category=category)
    idea_wo_category = idea_factory()

    mixin = ItemExportWithCategoriesMixin()

    virtual = mixin.get_virtual_fields({})
    assert "category" in virtual

    data = mixin.get_category_data(idea)
    assert category.name in data

    data_wo_category = mixin.get_category_data(idea_wo_category)
    assert "" == data_wo_category


@pytest.mark.django_db
def test_item_labels_mixin(idea_factory, label_factory):
    label1 = label_factory()
    label2 = label_factory(module=label1.module)
    idea = idea_factory.create(labels=(label1, label2))
    idea.save()
    idea_wo_label = idea_factory()

    mixin = ItemExportWithLabelsMixin()

    virtual = mixin.get_virtual_fields({})
    assert "labels" in virtual

    data = mixin.get_labels_data(idea)
    assert label1.name in data
    assert label2.name in data

    data_wo_label = mixin.get_labels_data(idea_wo_label)
    assert "" == data_wo_label


@pytest.mark.django_db
def test_reference_number_mixin(idea, question):
    mixin = ItemExportWithReferenceNumberMixin()

    virtual = mixin.get_virtual_fields({})
    assert "reference_number" in virtual

    assert idea.reference_number == mixin.get_reference_number_data(idea)
    assert "" == mixin.get_reference_number_data(question)


@pytest.mark.django_db
def test_moderator_feedback_mixin(idea):
    mixin = ItemExportWithModeratorFeedback()

    virtual = mixin.get_virtual_fields({})
    assert "moderator_status" in virtual
    assert "moderator_feedback_text" in virtual

    assert mixin.get_moderator_status_data(idea) == idea.get_moderator_status_display()

    assert (
        mixin.get_moderator_feedback_text_data(idea)
        == idea.moderator_feedback_text.feedback_text
    )
