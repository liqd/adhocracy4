import pytest
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from adhocracy4.comments.models import Comment
from tests.apps.questions.models import Question


@pytest.mark.django_db
def test_serializer(apiclient, question, comment_factory, rating_factory, user):
    question_ct = ContentType.objects.get_for_model(Question)
    comment_ct = ContentType.objects.get_for_model(Comment)
    moderator = question.project.moderators.first()

    comment = comment_factory(pk=1, content_object=question, creator=user)
    rating = rating_factory(content_object=comment, value=1, creator=user)
    comment_factory(
        pk=2, content_object=question, creator=user, comment_categories="QUE"
    )
    comment_factory(
        pk=3,
        content_object=question,
        creator=user,
        is_blocked=True,
        comment_categories="QUE",
    )
    comment_factory(pk=4, content_object=question, creator=user, is_censored=True)
    comment_factory(pk=5, content_object=question, creator=user, is_removed=True)
    comment_factory(
        pk=6, content_object=question, creator=user, is_moderator_marked=True
    )
    comment = comment_factory(pk=7, content_object=question, creator=moderator)
    comment_factory(pk=8, content_object=comment, creator=user)

    apiclient.force_authenticate(user=user)
    url = reverse(
        "comments_async-list",
        kwargs={"content_type": question_ct.pk, "object_pk": question.pk},
    )
    response = apiclient.get(url)

    comment_data = response.data["results"]
    assert len(comment_data) == 7

    # Testing a plain comment
    comment_1 = comment_data[6]
    assert comment_1["id"] == 1
    # returns get_short_name() of user, doesn't exist in django auth user
    assert comment_1["user_name"] == ""
    # django auth user model does not define get_absolute_url()
    assert comment_1["user_profile_url"] == ""
    assert comment_1["user_image"] is None
    assert comment_1["is_deleted"] is False
    assert comment_1["author_is_moderator"] is False
    assert len(comment_1["child_comments"]) == 0
    assert comment_1["comment"] == Comment.objects.get(pk=1).comment
    assert comment_1["object_pk"] == question.pk
    assert comment_1["is_removed"] is False
    assert comment_1["is_censored"] is False
    assert comment_1["is_blocked"] is False
    assert len(comment_1["comment_categories"]) == 0
    assert comment_1["last_discussed"] is None
    assert comment_1["is_moderator_marked"] is False
    assert comment_1["content_type"] == question_ct.pk
    assert comment_1["ratings"]["positive_ratings"] == 1
    assert comment_1["ratings"]["negative_ratings"] == 0
    assert comment_1["ratings"]["current_user_rating_value"] == 1
    assert comment_1["ratings"]["current_user_rating_id"] == rating.pk

    # Testing comment with a defined category:
    comment_2 = comment_data[5]
    assert comment_2["id"] == 2
    assert comment_2["user_name"] == ""
    assert comment_2["user_profile_url"] == ""
    assert comment_2["user_image"] is None
    assert comment_2["is_deleted"] is False
    assert comment_2["author_is_moderator"] is False
    assert len(comment_2["child_comments"]) == 0
    assert comment_2["comment"] == Comment.objects.get(pk=2).comment
    assert comment_2["object_pk"] == question.pk
    assert comment_2["is_removed"] is False
    assert comment_2["is_censored"] is False
    assert comment_2["is_blocked"] is False
    assert len(comment_2["comment_categories"]) == 1
    assert comment_2["comment_categories"] == {"QUE": "Question"}
    assert comment_2["last_discussed"] is None
    assert comment_2["is_moderator_marked"] is False
    assert comment_2["content_type"] == question_ct.pk
    assert comment_2["ratings"]["positive_ratings"] == 0
    assert comment_2["ratings"]["negative_ratings"] == 0
    assert comment_2["ratings"]["current_user_rating_value"] is None
    assert comment_2["ratings"]["current_user_rating_id"] is None

    # Testing a comment that is set to blocked by a moderator:
    comment_3 = comment_data[4]
    assert comment_3["id"] == 3
    assert comment_3["user_name"] == "unknown user"
    assert comment_3["user_profile_url"] == ""
    assert comment_3["user_image"] is None
    assert comment_3["is_deleted"] is True
    assert comment_3["author_is_moderator"] is False
    assert len(comment_3["child_comments"]) == 0
    assert comment_3["comment"] != Comment.objects.get(pk=3).comment
    assert comment_3["comment"] == ""
    assert comment_3["object_pk"] == question.pk
    assert comment_3["is_removed"] is False
    assert comment_3["is_censored"] is False
    assert comment_3["is_blocked"] is True
    assert len(comment_3["comment_categories"]) == 0
    assert comment_3["last_discussed"] is None
    assert comment_3["is_moderator_marked"] is False
    assert comment_3["content_type"] == question_ct.pk

    # Testing a comment that has been censored (deleted) by a moderator:
    comment_4 = comment_data[3]
    assert comment_4["id"] == 4
    assert comment_4["user_name"] == "unknown user"
    assert comment_4["user_profile_url"] == ""
    assert comment_4["user_image"] is None
    assert comment_4["is_deleted"] is True
    assert comment_4["author_is_moderator"] is False
    assert len(comment_4["child_comments"]) == 0
    assert comment_4["comment"] == Comment.objects.get(pk=4).comment
    assert comment_4["comment"] == ""
    assert comment_4["object_pk"] == question.pk
    assert comment_4["is_removed"] is False
    assert comment_4["is_censored"] is True
    assert comment_4["is_blocked"] is False
    assert len(comment_4["comment_categories"]) == 0
    assert comment_4["last_discussed"] is None
    assert comment_4["is_moderator_marked"] is False
    assert comment_4["content_type"] == question_ct.pk

    # Testing a comment that has been removed (deleted) by its creator:
    comment_5 = comment_data[2]
    assert comment_5["id"] == 5
    assert comment_5["user_name"] == "unknown user"
    assert comment_5["user_profile_url"] == ""
    assert comment_5["user_image"] is None
    assert comment_5["is_deleted"] is True
    assert comment_5["author_is_moderator"] is False
    assert len(comment_5["child_comments"]) == 0
    assert comment_5["comment"] == Comment.objects.get(pk=5).comment
    assert comment_5["comment"] == ""
    assert comment_5["object_pk"] == question.pk
    assert comment_5["is_removed"] is True
    assert comment_5["is_censored"] is False
    assert comment_5["is_blocked"] is False
    assert len(comment_5["comment_categories"]) == 0
    assert comment_5["last_discussed"] is None
    assert comment_5["is_moderator_marked"] is False
    assert comment_5["content_type"] == question_ct.pk

    # Testing a comment that has been marked by a moderator
    comment_6 = comment_data[1]
    assert comment_6["id"] == 6
    assert comment_6["user_name"] == ""
    assert comment_6["user_profile_url"] == ""
    assert comment_6["user_image"] is None
    assert comment_6["is_deleted"] is False
    assert comment_6["author_is_moderator"] is False
    assert len(comment_6["child_comments"]) == 0
    assert comment_6["comment"] == Comment.objects.get(pk=6).comment
    assert comment_6["object_pk"] == question.pk
    assert comment_6["is_removed"] is False
    assert comment_6["is_censored"] is False
    assert comment_6["is_blocked"] is False
    assert len(comment_6["comment_categories"]) == 0
    assert comment_6["last_discussed"] is None
    assert comment_6["is_moderator_marked"] is True
    assert comment_6["content_type"] == question_ct.pk

    # Testing a comment added by a moderator with child-comments:
    comment_7 = comment_data[0]
    assert comment_7["id"] == 7
    assert comment_7["is_deleted"] is False
    assert comment_7["author_is_moderator"] is True
    assert comment_7["user_image"] is None
    assert len(comment_7["child_comments"]) == 1
    assert comment_7["comment"] == Comment.objects.get(pk=7).comment
    assert comment_7["object_pk"] == question.pk
    assert comment_7["is_removed"] is False
    assert comment_7["is_censored"] is False
    assert comment_7["is_blocked"] is False
    assert len(comment_7["comment_categories"]) == 0
    assert comment_7["last_discussed"] is None
    assert comment_7["is_moderator_marked"] is False
    assert comment_7["content_type"] == question_ct.pk

    # Testing a child-comment:
    comment_8 = comment_7["child_comments"][0]
    assert comment_8["id"] == 8
    assert comment_8["is_deleted"] is False
    assert comment_8["author_is_moderator"] is False
    assert comment_8["user_image"] is None
    assert comment_8["comment"] == Comment.objects.get(pk=8).comment
    assert comment_8["object_pk"] == comment.pk
    assert comment_8["is_removed"] is False
    assert comment_8["is_censored"] is False
    assert comment_8["is_blocked"] is False
    assert len(comment_8["comment_categories"]) == 0
    assert comment_8["last_discussed"] is None
    assert comment_8["is_moderator_marked"] is False
    assert comment_8["content_type"] == comment_ct.pk
