import pytest
from django.db import IntegrityError


@pytest.mark.django_db
def test_rating_value(rating):
    assert rating.value >= -1 and rating.value <= 1


@pytest.mark.django_db
def test_rating_value_cannot_be_greater_1(rating_factory):
    rating = rating_factory(value=10)
    assert rating.value == 1


@pytest.mark.django_db
def test_rating_value_cannot_be_smaller_mius1(rating_factory):
    rating = rating_factory(value=-10)
    assert rating.value == -1


@pytest.mark.django_db
def test_rating_value_can_be_1(rating_factory):
    rating = rating_factory(value=1)
    assert rating.value == 1


@pytest.mark.django_db
def test_rating_value_can_be_0(rating_factory):
    rating = rating_factory(value=0)
    assert rating.value == 0


@pytest.mark.django_db
def test_rating_value_can_be_minus1(rating_factory):
    rating = rating_factory(value=-1)
    assert rating.value == -1


@pytest.mark.django_db
def test_user_can_rating_once(rating_factory, rating, user):

    with pytest.raises(Exception) as e:
        rating_factory(
            value=1,
            creator=rating.creator,
            content_object=rating.content_object,
        )

    assert e.type == IntegrityError


@pytest.mark.django_db
def test_str(rating):
    assert str(rating) == '1'


@pytest.mark.django_db
def test_get_meta_info(rating, user_factory):
    meta_info = {
        'positive_ratings_on_same_object': 1,
        'negative_ratings_on_same_object': 0,
        'user_rating_on_same_object_value': None,
        'user_rating_on_same_object_id': None,
    }

    assert rating.get_meta_info(user_factory()) == meta_info

    own_meta_info = {
        'positive_ratings_on_same_object': 1,
        'negative_ratings_on_same_object': 0,
        'user_rating_on_same_object_value': 1,
        'user_rating_on_same_object_id': rating.id,
    }
    assert rating.get_meta_info(rating.creator) == own_meta_info
