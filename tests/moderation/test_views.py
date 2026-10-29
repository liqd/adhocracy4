import pytest
from django.urls import reverse

from tests.apps.ideas.factories import IdeaFactory
from tests.comments.factories import CommentFactory


@pytest.fixture
def moderated_project(project_factory, user):
    return project_factory(moderators=[user])


@pytest.fixture
def other_project(project_factory):
    return project_factory()


@pytest.mark.django_db
def test_dashboard_lists_only_moderated_projects(
    client, user, moderated_project, other_project
):
    client.login(username=user.username, password="password")

    response = client.get(reverse("a4moderation:dashboard"))

    assert response.status_code == 200
    projects = list(response.context["moderated_projects"])
    assert moderated_project in projects
    assert other_project not in projects


@pytest.mark.django_db
def test_dashboard_requires_login(client):
    response = client.get(reverse("a4moderation:dashboard"))

    assert response.status_code == 302


@pytest.mark.django_db
def test_project_view_allowed_for_moderator(client, user, moderated_project):
    client.login(username=user.username, password="password")

    response = client.get(
        reverse("a4moderation:project", kwargs={"project_pk": moderated_project.pk})
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_project_view_forbidden_for_other_user(client, another_user, moderated_project):
    client.login(username=another_user.username, password="password")

    response = client.get(
        reverse("a4moderation:project", kwargs={"project_pk": moderated_project.pk})
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_project_view_lists_comments_and_ideas(
    client, user, moderated_project, module_factory
):
    module = module_factory(project=moderated_project)
    idea = IdeaFactory(module=module, description="An <b>idea</b>")
    comment = CommentFactory(content_object=idea, creator=user)
    idea.is_reviewed = True
    idea.save(update_fields=["is_reviewed"])
    comment.is_reviewed = True
    comment.save(update_fields=["is_reviewed"])
    client.login(username=user.username, password="password")

    response = client.get(
        reverse("a4moderation:project", kwargs={"project_pk": moderated_project.pk}),
        {"state": "all"},
    )

    item_types = {item["type"] for item in response.context["items"]}
    assert item_types == {"a4comments.comment", "a4test_ideas.idea"}


@pytest.mark.django_db
def test_project_view_filters_unread_items(
    client, user, moderated_project, module_factory
):
    module = module_factory(project=moderated_project)
    read_idea = IdeaFactory(module=module, is_reviewed=True)
    unread_idea = IdeaFactory(module=module, is_reviewed=False)
    client.login(username=user.username, password="password")

    response = client.get(
        reverse("a4moderation:project", kwargs={"project_pk": moderated_project.pk}),
        {"state": "unread"},
    )

    item_pks = {item["pk"] for item in response.context["items"]}
    assert unread_idea.pk in item_pks
    assert read_idea.pk not in item_pks


@pytest.mark.django_db
def test_project_view_orders_newest_first(
    client, user, moderated_project, module_factory
):
    module = module_factory(project=moderated_project)
    first = IdeaFactory(module=module)
    second = IdeaFactory(module=module)
    client.login(username=user.username, password="password")

    response = client.get(
        reverse("a4moderation:project", kwargs={"project_pk": moderated_project.pk}),
        {"state": "all", "ordering": "newest"},
    )

    pks = [item["pk"] for item in response.context["items"]]
    assert pks.index(second.pk) < pks.index(first.pk)


@pytest.mark.django_db
def test_mark_item_as_read(client, user, moderated_project, module_factory):
    module = module_factory(project=moderated_project)
    idea = IdeaFactory(module=module, is_reviewed=False)
    client.login(username=user.username, password="password")

    response = client.post(
        reverse(
            "a4moderation:item-read",
            kwargs={
                "project_pk": moderated_project.pk,
                "item_type": "a4test_ideas.idea",
                "pk": idea.pk,
            },
        ),
        {"read": "1", "state": "all"},
        HTTP_HX_REQUEST="true",
    )

    idea.refresh_from_db()
    assert response.status_code == 200
    assert idea.is_reviewed is True
    assert "moderationItemUpdated" in response["HX-Trigger"]


@pytest.mark.django_db
def test_mark_item_as_read_removes_item_from_unread_filter(
    client, user, moderated_project, module_factory
):
    module = module_factory(project=moderated_project)
    idea = IdeaFactory(module=module, is_reviewed=False)
    client.login(username=user.username, password="password")

    response = client.post(
        reverse(
            "a4moderation:item-read",
            kwargs={
                "project_pk": moderated_project.pk,
                "item_type": "a4test_ideas.idea",
                "pk": idea.pk,
            },
        ),
        {"read": "1", "state": "unread"},
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 200
    assert response.content == b""


@pytest.mark.django_db
def test_mark_item_of_other_project_is_not_found(
    client, user, moderated_project, other_project, module_factory
):
    other_module = module_factory(project=other_project)
    idea = IdeaFactory(module=other_module)
    client.login(username=user.username, password="password")

    response = client.post(
        reverse(
            "a4moderation:item-read",
            kwargs={
                "project_pk": moderated_project.pk,
                "item_type": "a4test_ideas.idea",
                "pk": idea.pk,
            },
        ),
        {"read": "1"},
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_project_view_paginates_items(client, user, moderated_project, module_factory):
    module = module_factory(project=moderated_project)
    for _ in range(21):
        IdeaFactory(module=module)
    client.login(username=user.username, password="password")

    first_page = client.get(
        reverse("a4moderation:project", kwargs={"project_pk": moderated_project.pk}),
        {"state": "all"},
    )
    second_page = client.get(
        reverse("a4moderation:project", kwargs={"project_pk": moderated_project.pk}),
        {"state": "all", "page": 2},
    )

    assert len(first_page.context["items"]) == 20
    assert len(second_page.context["items"]) == 1


@pytest.mark.django_db
def test_project_view_filters_content_type(
    client, user, moderated_project, module_factory
):
    module = module_factory(project=moderated_project)
    idea = IdeaFactory(module=module)
    CommentFactory(content_object=idea)
    client.login(username=user.username, password="password")

    response = client.get(
        reverse("a4moderation:project", kwargs={"project_pk": moderated_project.pk}),
        {"state": "all", "content_type": "comments"},
    )

    assert {item["type"] for item in response.context["items"]} == {
        "a4comments.comment"
    }


@pytest.mark.django_db
def test_project_view_filters_read_items(
    client, user, moderated_project, module_factory
):
    module = module_factory(project=moderated_project)
    read_idea = IdeaFactory(module=module, is_reviewed=True)
    IdeaFactory(module=module, is_reviewed=False)
    client.login(username=user.username, password="password")

    response = client.get(
        reverse("a4moderation:project", kwargs={"project_pk": moderated_project.pk}),
        {"state": "read"},
    )

    assert [item["pk"] for item in response.context["items"]] == [read_idea.pk]


@pytest.mark.django_db
def test_item_key_can_be_used_as_html_id(
    client, user, moderated_project, module_factory
):
    module = module_factory(project=moderated_project)
    IdeaFactory(module=module)
    client.login(username=user.username, password="password")

    response = client.get(
        reverse("a4moderation:project", kwargs={"project_pk": moderated_project.pk}),
        {"state": "all"},
    )

    assert "." not in response.context["items"][0]["key"]


@pytest.mark.django_db
def test_mark_item_as_unread(client, user, moderated_project, module_factory):
    module = module_factory(project=moderated_project)
    idea = IdeaFactory(module=module, is_reviewed=True)
    client.login(username=user.username, password="password")

    response = client.post(
        reverse(
            "a4moderation:item-read",
            kwargs={
                "project_pk": moderated_project.pk,
                "item_type": "a4test_ideas.idea",
                "pk": idea.pk,
            },
        ),
        {"read": "0", "state": "all"},
        HTTP_HX_REQUEST="true",
    )

    idea.refresh_from_db()
    assert response.status_code == 200
    assert idea.is_reviewed is False


@pytest.mark.django_db
def test_feedback_form_is_prefilled(client, user, moderated_project, module_factory):
    module = module_factory(project=moderated_project)
    idea = IdeaFactory(module=module, is_reviewed=False)
    client.login(username=user.username, password="password")

    response = client.get(
        reverse(
            "a4moderation:item-feedback",
            kwargs={
                "project_pk": moderated_project.pk,
                "item_type": "a4test_ideas.idea",
                "pk": idea.pk,
            },
        ),
        {"state": "unread"},
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 200
    assert b'name="moderator_status"' in response.content
    assert b'name="feedback_text"' in response.content
    assert b'name="state" value="unread"' in response.content


@pytest.mark.django_db
def test_save_feedback_updates_item_and_marks_it_read(
    client, user, moderated_project, module_factory
):
    module = module_factory(project=moderated_project)
    idea = IdeaFactory(module=module, is_reviewed=False)
    client.login(username=user.username, password="password")

    response = client.post(
        reverse(
            "a4moderation:item-feedback",
            kwargs={
                "project_pk": moderated_project.pk,
                "item_type": "a4test_ideas.idea",
                "pk": idea.pk,
            },
        ),
        {"moderator_status": "CONSIDERATION", "feedback_text": "Great idea"},
        HTTP_HX_REQUEST="true",
    )

    idea.refresh_from_db()
    assert response.status_code == 200
    assert response["HX-Retarget"] == "#moderation-item-a4test_ideas_idea-{}".format(
        idea.pk
    )
    assert idea.moderator_status == "CONSIDERATION"
    assert idea.moderator_feedback_text.feedback_text == "<p>Great idea</p>"
    assert idea.is_reviewed is True


@pytest.mark.django_db
def test_feedback_is_not_available_for_comments(
    client, user, moderated_project, module_factory
):
    module = module_factory(project=moderated_project)
    idea = IdeaFactory(module=module)
    comment = CommentFactory(content_object=idea)
    client.login(username=user.username, password="password")

    response = client.get(
        reverse(
            "a4moderation:item-feedback",
            kwargs={
                "project_pk": moderated_project.pk,
                "item_type": "a4comments.comment",
                "pk": comment.pk,
            },
        )
    )

    assert response.status_code == 404
