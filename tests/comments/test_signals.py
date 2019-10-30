import pytest
from django.core.exceptions import ObjectDoesNotExist

from adhocracy4.comments import models


@pytest.mark.django_db
def test_delete_of_content_object(comment):
    question = comment.content_object
    question.delete()

    with pytest.raises(ObjectDoesNotExist):
        models.Comment.objects.get(id=comment.id)
