import pytest
from django.core.exceptions import ObjectDoesNotExist

from adhocracy4.comments import models


@pytest.mark.django_db
def test_delete_of_content_object(comment, child_comment_factory):
    child_comment = child_comment_factory(content_object=comment)
    question = comment.content_object
    question.delete()

    with pytest.raises(ObjectDoesNotExist):
        models.Comment.objects.get(id=comment.id)

    with pytest.raises(ObjectDoesNotExist):
        models.Comment.objects.get(id=child_comment.id)


@pytest.mark.django_db
def test_update_last_discussed(comment_factory, question):

    assert question.last_discussed is None

    comment = comment_factory(content_object=question)
    comment.save()
    question.refresh_from_db()
    assert question.last_discussed == comment.created

    child_comment = comment_factory(content_object=comment)
    child_comment.save()
    question.refresh_from_db()
    assert question.last_discussed == child_comment.created
