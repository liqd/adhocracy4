import pytest
from django.urls import reverse

from adhocracy4.moderation import utils
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
def test_feedback_for_comments_is_stored_as_child_comment(
    client, user, moderated_project, module_factory
):
    module = module_factory(project=moderated_project)
    idea = IdeaFactory(module=module)
    comment = CommentFactory(content_object=idea)
    client.login(username=user.username, password="password")

    response = client.post(
        reverse(
            "a4moderation:item-feedback",
            kwargs={
                "project_pk": moderated_project.pk,
                "item_type": "a4comments.comment",
                "pk": comment.pk,
            },
        ),
        {"feedback_text": "Antwort auf den Kommentar"},
        HTTP_HX_REQUEST="true",
    )

    comment.refresh_from_db()
    child = comment.child_comments.get()
    assert response.status_code == 200
    assert child.comment == "Antwort auf den Kommentar"
    assert child.creator == user
    assert comment.is_reviewed is True
    assert utils.build_moderation_item(comment)["feedback"] == child.comment

    rows = utils.get_moderation_queryset(moderated_project)
    comment_rows = [row for row in rows if row["item_type"] == "a4comments.comment"]
    assert child.pk not in [row["pk"] for row in comment_rows]


@pytest.mark.django_db
def test_comment_feedback_leaves_unread_filter(
    client, user, moderated_project, module_factory
):
    module = module_factory(project=moderated_project)
    idea = IdeaFactory(module=module)
    comment = CommentFactory(content_object=idea, is_reviewed=False)
    client.login(username=user.username, password="password")

    response = client.post(
        reverse(
            "a4moderation:item-feedback",
            kwargs={
                "project_pk": moderated_project.pk,
                "item_type": "a4comments.comment",
                "pk": comment.pk,
            },
        ),
        {"feedback_text": "Neu", "state": "unread"},
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 200
    assert response.content == b""
    assert response["HX-Retarget"] == "#moderation-item-a4comments_comment-{}".format(
        comment.pk
    )


@pytest.mark.django_db
def test_feedback_edit_keeps_unchanged_html(
    client, user, moderated_project, module_factory
):
    module = module_factory(project=moderated_project)
    idea = IdeaFactory(module=module, is_reviewed=True)
    idea.moderator_feedback_text.feedback_text = "<p>Alt &amp; neu</p>"
    idea.moderator_feedback_text.save()
    idea.save()
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
        {"moderator_status": "ACCEPTED", "feedback_text": "Alt & neu"},
        HTTP_HX_REQUEST="true",
    )

    idea.refresh_from_db()
    assert response.status_code == 200
    assert idea.moderator_feedback_text.feedback_text == "<p>Alt &amp; neu</p>"


@pytest.mark.django_db
def test_saved_feedback_leaves_unread_filter(
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
        {"feedback_text": "Neu", "state": "unread"},
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 200
    assert response.content == b""
    assert response["HX-Retarget"]


@pytest.mark.django_db
def test_mark_item_as_resolved_and_reopen(
    client, user, moderated_project, module_factory
):
    module = module_factory(project=moderated_project)
    idea = IdeaFactory(module=module)
    client.login(username=user.username, password="password")
    url = reverse(
        "a4moderation:item-resolve",
        kwargs={
            "project_pk": moderated_project.pk,
            "item_type": "a4test_ideas.idea",
            "pk": idea.pk,
        },
    )

    response = client.post(url, {"resolved": "1"}, HTTP_HX_REQUEST="true")
    idea.refresh_from_db()
    assert response.status_code == 200
    assert idea.is_resolved is True
    assert idea.resolved_at is not None

    response = client.post(url, {"resolved": "0"}, HTTP_HX_REQUEST="true")
    idea.refresh_from_db()
    assert response.status_code == 200
    assert idea.is_resolved is False
    assert idea.resolved_at is None


@pytest.mark.django_db
def test_resolved_items_are_listed_in_resolved_state(
    client, user, moderated_project, module_factory
):
    module = module_factory(project=moderated_project)
    resolved = IdeaFactory(module=module, is_resolved=True)
    IdeaFactory(module=module, is_resolved=False)
    client.login(username=user.username, password="password")

    response = client.get(
        reverse("a4moderation:project", kwargs={"project_pk": moderated_project.pk}),
        {"state": "resolved"},
    )

    assert [item["pk"] for item in response.context["items"]] == [resolved.pk]


@pytest.mark.django_db
def test_delete_comment(client, user, moderated_project, module_factory):
    module = module_factory(project=moderated_project)
    idea = IdeaFactory(module=module)
    comment = CommentFactory(content_object=idea, comment="To be deleted")
    client.login(username=user.username, password="password")
    url = reverse(
        "a4moderation:item-delete",
        kwargs={
            "project_pk": moderated_project.pk,
            "item_type": "a4comments.comment",
            "pk": comment.pk,
        },
    )

    response = client.post(url, {}, HTTP_HX_REQUEST="true")

    comment.refresh_from_db()
    assert response.status_code == 200
    assert comment.is_censored is True
    assert comment.comment == ""


@pytest.mark.django_db
def test_delete_idea(client, user, moderated_project, module_factory):
    from adhocracy4.reports.models import Report
    from tests.reports.factories import ReportFactory

    module = module_factory(project=moderated_project)
    idea = IdeaFactory(module=module)
    report = ReportFactory(content_object=idea)
    client.login(username=user.username, password="password")
    url = reverse(
        "a4moderation:item-delete",
        kwargs={
            "project_pk": moderated_project.pk,
            "item_type": "a4test_ideas.idea",
            "pk": idea.pk,
        },
    )

    response = client.post(url, {}, HTTP_HX_REQUEST="true")

    assert response.status_code == 200
    assert response.content == b""
    assert not idea.__class__.objects.filter(pk=idea.pk).exists()
    assert not Report.objects.filter(pk=report.pk).exists()
    assert response["HX-Trigger"]


@pytest.mark.django_db
def test_edit_comment(client, user, moderated_project, module_factory):
    module = module_factory(project=moderated_project)
    idea = IdeaFactory(module=module)
    comment = CommentFactory(content_object=idea, comment="Old text")
    client.login(username=user.username, password="password")
    url = reverse(
        "a4moderation:item-edit",
        kwargs={
            "project_pk": moderated_project.pk,
            "item_type": "a4comments.comment",
            "pk": comment.pk,
        },
    )

    response = client.post(url, {"comment": "New text"}, HTTP_HX_REQUEST="true")

    comment.refresh_from_db()
    assert response.status_code == 200
    assert comment.comment == "New text"
    assert comment.is_reviewed is True


@pytest.mark.django_db
def test_edit_comment_cancel_returns_item(
    client, user, moderated_project, module_factory
):
    module = module_factory(project=moderated_project)
    idea = IdeaFactory(module=module)
    comment = CommentFactory(content_object=idea, comment="Old text")
    client.login(username=user.username, password="password")
    url = reverse(
        "a4moderation:item-edit",
        kwargs={
            "project_pk": moderated_project.pk,
            "item_type": "a4comments.comment",
            "pk": comment.pk,
        },
    )

    response = client.get(url, {"cancel": "1"}, HTTP_HX_REQUEST="true")

    assert response.status_code == 200
    assert b'id="moderation-item-a4comments_comment-' in response.content
    assert not response.context.get("edit_mode")
    assert "form" not in response.context


@pytest.mark.django_db
def test_report_count(client, user, moderated_project, module_factory):
    from tests.reports.factories import ReportFactory

    module = module_factory(project=moderated_project)
    idea = IdeaFactory(module=module)
    comment = CommentFactory(content_object=idea)
    ReportFactory(content_object=idea)
    ReportFactory(content_object=comment)
    client.login(username=user.username, password="password")

    response = client.get(
        reverse("a4moderation:project", kwargs={"project_pk": moderated_project.pk}),
        {"state": "all"},
    )

    counts = {item["type"]: item["num_reports"] for item in response.context["items"]}
    assert counts["a4test_ideas.idea"] == 1
    assert counts["a4comments.comment"] == 1
