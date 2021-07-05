import pytest

from adhocracy4.exports import mixins


@pytest.mark.django_db
def test_moderator_feedback_mixin(proposal):
    mixin = mixins.ItemExportWithModeratorFeedback()

    virtual = mixin.get_virtual_fields({})
    assert 'moderator_feedback' in virtual
    assert 'moderator_statement' in virtual

    assert mixin.get_moderator_feedback_data(proposal)\
        == proposal.get_moderator_feedback_display()

    assert mixin.get_moderator_statement_data(proposal)\
        == proposal.moderator_statement.statement


@pytest.mark.django_db
def test_user_generated_content_mixin(idea):
    mixin = mixins.UserGeneratedContentExportMixin()

    virtual = mixin.get_virtual_fields({})
    assert 'creator' in virtual
    assert 'created' in virtual

    assert idea.creator.username == mixin.get_creator_data(idea)
    assert idea.created.isoformat() == mixin.get_created_data(idea)


@pytest.mark.django_db
def test_reference_number_mixin(idea):
    mixin = mixins.ItemExportWithReferenceNumberMixin()

    virtual = mixin.get_virtual_fields({})
    assert 'reference_number' in virtual

    assert idea.reference_number == mixin.get_reference_number_data(idea)
