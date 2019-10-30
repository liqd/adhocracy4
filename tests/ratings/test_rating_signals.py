import pytest
from django.core.exceptions import ObjectDoesNotExist

from adhocracy4.ratings import models


@pytest.mark.django_db
def test_delete_of_content_object(rating):
    question = rating.content_object
    question.delete()

    with pytest.raises(ObjectDoesNotExist):
        models.Rating.objects.get(id=rating.id)
