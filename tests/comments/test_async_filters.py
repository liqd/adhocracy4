import pytest
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from tests.apps.questions.models import Question


@pytest.mark.django_db
def test_category_filter(apiclient, question, comment_factory, user):
    question_ct = ContentType.objects.get_for_model(Question)

    comment_factory(pk=1, content_object=question, comment_categories="QUE, REM")
    comment_factory(pk=2, content_object=question, comment_categories="QUE")
    comment_factory(
        pk=3, content_object=question, is_blocked=True, comment_categories="QUE"
    )
    comment_factory(
        pk=4, content_object=question, is_censored=True, comment_categories="REM"
    )
    comment_factory(
        pk=5, content_object=question, is_removed=True, comment_categories="QUE, REM"
    )
    comment_factory(pk=6, content_object=question, comment_categories="REM")
    comment = comment_factory(pk=7, content_object=question, comment_categories="QUE")
    comment_factory(pk=8, content_object=comment, creator=user)

    apiclient.force_authenticate(user=user)
    url = reverse(
        "comments_async-list",
        kwargs={"content_type": question_ct.pk, "object_pk": question.pk},
    )
    response = apiclient.get(url)

    comment_data = response.data["results"]
    assert len(comment_data) == 7

    url = reverse(
        "comments_async-list",
        kwargs={"content_type": question_ct.pk, "object_pk": question.pk},
    )
    url += "?comment_category=QUE"
    response = apiclient.get(url)
    print(response)

    comment_data = response.data["results"]
    assert len(comment_data) == 3
    assert comment_data[2]["id"] == 1
    assert comment_data[1]["id"] == 2
    assert comment_data[0]["id"] == 7

    url = reverse(
        "comments_async-list",
        kwargs={"content_type": question_ct.pk, "object_pk": question.pk},
    )
    url += "?comment_category=REM"
    response = apiclient.get(url)

    comment_data = response.data["results"]
    assert len(comment_data) == 2
    assert comment_data[1]["id"] == 1
    assert comment_data[0]["id"] == 6

    url = reverse(
        "comments_async-list",
        kwargs={"content_type": question_ct.pk, "object_pk": question.pk},
    )
    url += "?comment_category="
    response = apiclient.get(url)

    comment_data = response.data["results"]
    assert len(comment_data) == 7


@pytest.mark.django_db
def test_search_filter(apiclient, question, comment_factory, user):
    question_ct = ContentType.objects.get_for_model(Question)

    comment_factory(pk=1, content_object=question, comment="Lorem ipsum")
    comment_factory(pk=2, content_object=question, comment="dolor sit amet")
    comment_factory(
        pk=3, content_object=question, is_blocked=True, comment="Lorem ipsum"
    )
    comment_factory(
        pk=4, content_object=question, is_censored=True, comment="Lorem ipsum"
    )
    comment_factory(
        pk=5, content_object=question, is_removed=True, comment="Lorem ipsum"
    )
    comment_factory(pk=6, content_object=question, comment="Lorem ipsum dolor sit amet")
    comment = comment_factory(
        pk=7, content_object=question, comment="ipsum dolor sit amet"
    )
    comment_factory(pk=8, content_object=comment, creator=user, comment="Lorem ipsum")

    apiclient.force_authenticate(user=user)
    url = reverse(
        "comments_async-list",
        kwargs={"content_type": question_ct.pk, "object_pk": question.pk},
    )
    response = apiclient.get(url)
    comment_data = response.data["results"]
    assert len(comment_data) == 7

    url = reverse(
        "comments_async-list",
        kwargs={"content_type": question_ct.pk, "object_pk": question.pk},
    )
    url += "?search=lorem+ipsum"
    response = apiclient.get(url)
    comment_data = response.data["results"]
    assert len(comment_data) == 2
    assert comment_data[1]["id"] == 1
    assert comment_data[0]["id"] == 6

    url = reverse(
        "comments_async-list",
        kwargs={"content_type": question_ct.pk, "object_pk": question.pk},
    )
    url += "?search=lorem"
    response = apiclient.get(url)
    comment_data = response.data["results"]
    assert len(comment_data) == 2
    assert comment_data[1]["id"] == 1
    assert comment_data[0]["id"] == 6

    url = reverse(
        "comments_async-list",
        kwargs={"content_type": question_ct.pk, "object_pk": question.pk},
    )
    url += "?search=ipsum"
    response = apiclient.get(url)
    comment_data = response.data["results"]
    assert len(comment_data) == 3
    assert comment_data[2]["id"] == 1
    assert comment_data[1]["id"] == 6
    assert comment_data[0]["id"] == 7

    url = reverse(
        "comments_async-list",
        kwargs={"content_type": question_ct.pk, "object_pk": question.pk},
    )
    url += "?search=lirum"
    response = apiclient.get(url)
    comment_data = response.data["results"]
    assert len(comment_data) == 0

    url = reverse(
        "comments_async-list",
        kwargs={"content_type": question_ct.pk, "object_pk": question.pk},
    )
    url += "?search="
    response = apiclient.get(url)
    comment_data = response.data["results"]
    assert len(comment_data) == 7


@pytest.mark.django_db
def test_ordering_filter(apiclient, question, comment_factory, rating_factory, user):
    question_ct = ContentType.objects.get_for_model(Question)

    comment1 = comment_factory(pk=1, content_object=question)
    comment2 = comment_factory(pk=2, content_object=question, is_moderator_marked=True)
    comment3 = comment_factory(pk=3, content_object=question)
    comment4 = comment_factory(pk=4, content_object=question, is_moderator_marked=True)
    comment_factory(pk=5, content_object=comment1)
    comment_factory(pk=6, content_object=comment1)
    comment_factory(pk=7, content_object=comment1)
    comment_factory(pk=8, content_object=comment2)
    comment_factory(pk=9, content_object=comment2)
    comment_factory(pk=10, content_object=comment3)

    rating_factory(content_object=comment2, value=1)
    rating_factory(content_object=comment2, value=-1)
    rating_factory(content_object=comment2, value=-1)
    rating_factory(content_object=comment1, value=1)
    rating_factory(content_object=comment1, value=1)
    rating_factory(content_object=comment3, value=1)
    rating_factory(content_object=comment4, value=-1)

    apiclient.force_authenticate(user=user)
    url = reverse(
        "comments_async-list",
        kwargs={"content_type": question_ct.pk, "object_pk": question.pk},
    )
    response = apiclient.get(url)
    comment_data = response.data["results"]
    assert len(comment_data) == 4
    assert comment_data[3]["id"] == 1
    assert comment_data[2]["id"] == 2
    assert comment_data[1]["id"] == 3
    assert comment_data[0]["id"] == 4

    apiclient.force_authenticate(user=user)
    url = reverse(
        "comments_async-list",
        kwargs={"content_type": question_ct.pk, "object_pk": question.pk},
    )
    url += "?ordering="
    response = apiclient.get(url)
    comment_data = response.data["results"]
    assert len(comment_data) == 4
    assert comment_data[3]["id"] == 1
    assert comment_data[2]["id"] == 2
    assert comment_data[1]["id"] == 3
    assert comment_data[0]["id"] == 4

    apiclient.force_authenticate(user=user)
    url = reverse(
        "comments_async-list",
        kwargs={"content_type": question_ct.pk, "object_pk": question.pk},
    )
    url += "?ordering=new"
    response = apiclient.get(url)
    comment_data = response.data["results"]
    assert len(comment_data) == 4
    assert comment_data[3]["id"] == 1
    assert comment_data[2]["id"] == 2
    assert comment_data[1]["id"] == 3
    assert comment_data[0]["id"] == 4

    url = reverse(
        "comments_async-list",
        kwargs={"content_type": question_ct.pk, "object_pk": question.pk},
    )
    url += "?ordering=ans"
    response = apiclient.get(url)
    comment_data = response.data["results"]
    assert len(comment_data) == 4
    assert comment_data[3]["id"] == 4
    assert comment_data[2]["id"] == 3
    assert comment_data[1]["id"] == 2
    assert comment_data[0]["id"] == 1

    url = reverse(
        "comments_async-list",
        kwargs={"content_type": question_ct.pk, "object_pk": question.pk},
    )
    url += "?ordering=pos"
    response = apiclient.get(url)
    comment_data = response.data["results"]
    assert len(comment_data) == 4
    assert comment_data[3]["id"] == 4
    assert comment_data[2]["id"] == 2
    assert comment_data[1]["id"] == 3
    assert comment_data[0]["id"] == 1

    url = reverse(
        "comments_async-list",
        kwargs={"content_type": question_ct.pk, "object_pk": question.pk},
    )
    url += "?ordering=neg"
    response = apiclient.get(url)
    comment_data = response.data["results"]
    assert len(comment_data) == 4
    assert comment_data[3]["id"] == 1
    assert comment_data[2]["id"] == 3
    assert comment_data[1]["id"] == 4
    assert comment_data[0]["id"] == 2

    url = reverse(
        "comments_async-list",
        kwargs={"content_type": question_ct.pk, "object_pk": question.pk},
    )
    url += "?ordering=dis"
    response = apiclient.get(url)
    comment_data = response.data["results"]
    assert len(comment_data) == 4
    assert comment_data[3]["id"] == 1
    assert comment_data[2]["id"] == 2
    assert comment_data[1]["id"] == 3
    assert comment_data[0]["id"] == 4

    url = reverse(
        "comments_async-list",
        kwargs={"content_type": question_ct.pk, "object_pk": question.pk},
    )
    url += "?ordering=mom"
    response = apiclient.get(url)
    comment_data = response.data["results"]
    assert len(comment_data) == 4
    assert comment_data[3]["id"] == 1
    assert comment_data[2]["id"] == 3
    assert comment_data[1]["id"] == 2
    assert comment_data[0]["id"] == 4
