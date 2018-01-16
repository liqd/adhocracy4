import pytest

from meinberlin.apps.exports import views


@pytest.mark.django_db
def test_moderator_feedback_mixin(proposal):
    mixin = views.ItemExportWithModeratorFeedback()

    virtual = mixin.get_virtual_fields({})
    assert 'moderator_feedback' in virtual
    assert 'moderator_statement' in virtual

    assert mixin.get_moderator_feedback_data(proposal)\
        == proposal.get_moderator_feedback_display()

    assert mixin.get_moderator_statement_data(proposal)\
        == proposal.moderator_statement.statement
