import re
from collections import defaultdict

from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import CharField
from django.db.models import Count
from django.db.models import Q
from django.db.models import Value
from django.utils.text import Truncator
from django.utils.translation import gettext as _

from adhocracy4 import transforms
from adhocracy4.comments.models import Comment
from adhocracy4.projects.models import Project
from adhocracy4.reports.models import Report

TRUNCATE_LENGTH = 500

STATE_ALL = "all"
STATE_READ = "read"
STATE_RESOLVED = "resolved"
STATE_UNREAD = "unread"
STATES = (STATE_ALL, STATE_UNREAD, STATE_RESOLVED, STATE_READ)

CONTENT_TYPE_ALL = "all"
CONTENT_TYPE_COMMENTS = "comments"
CONTENT_TYPE_ITEMS = "items"
CONTENT_TYPES = (CONTENT_TYPE_ALL, CONTENT_TYPE_COMMENTS, CONTENT_TYPE_ITEMS)

ORDERING_NEWEST = "newest"
ORDERING_OLDEST = "oldest"
ORDERINGS = (ORDERING_NEWEST, ORDERING_OLDEST)


def get_item_models():
    """Return the models configured as moderatable items."""
    itemables = getattr(settings, "A4_MODERATION_ITEMABLES", ())
    return [
        apps.get_model(app_label, model_name) for app_label, model_name in itemables
    ]


def get_moderated_projects(user):
    """Return all projects the user is allowed to moderate."""
    if not user or not user.is_authenticated:
        return Project.objects.none()

    if user.is_superuser:
        return Project.objects.select_related("organisation").order_by("name")

    query = Q(moderators=user) | Q(group__in=user.groups.all())

    initiator_organisations = getattr(user, "organisation_set", None)
    if initiator_organisations is not None:
        query |= Q(organisation__in=initiator_organisations.all())
    elif user.is_staff:
        # The default organisation implementation treats staff as initiators.
        return Project.objects.select_related("organisation").order_by("name")

    return (
        Project.objects.filter(query)
        .select_related("organisation")
        .distinct()
        .order_by("name")
    )


def user_moderates_any_project(user):
    return get_moderated_projects(user).exists()


def supports_hiding(item):
    """Return if the item can be hidden from the discussion."""
    return isinstance(item, Comment)


def supports_feedback(item):
    """Return if the item has a moderation status or official feedback."""
    if isinstance(item, Comment):
        return False
    field_names = {field.name for field in item._meta.get_fields()}
    return "moderator_status" in field_names or "moderator_feedback_text" in field_names


def _filter_state(queryset, state):
    if state == STATE_RESOLVED:
        return queryset.filter(is_resolved=True)
    if state == STATE_READ:
        return queryset.filter(is_reviewed=True, is_resolved=False)
    if state == STATE_UNREAD:
        return queryset.filter(is_reviewed=False, is_resolved=False)
    return queryset


def _comment_rows(project, state):
    comments = Comment.objects.filter(project=project)
    comments = _filter_state(comments, state)
    return (
        comments.annotate(
            item_type=Value(Comment._meta.label_lower, output_field=CharField())
        )
        .values("pk", "created", "item_type")
        .order_by()
    )


def _item_rows(model, project, state):
    items = model.objects.filter(module__project=project)
    items = _filter_state(items, state)
    return (
        items.annotate(
            item_type=Value(model._meta.label_lower, output_field=CharField())
        )
        .values("pk", "created", "item_type")
        .order_by()
    )


def get_moderation_queryset(
    project,
    content_type=CONTENT_TYPE_ALL,
    state=STATE_ALL,
    ordering=ORDERING_NEWEST,
):
    """Return a union of comments and items for a project.

    The result is a queryset of rows with the columns ``pk``, ``created``
    and ``item_type`` so it can be paginated and sorted in the database.
    """
    row_sets = []
    if content_type in (CONTENT_TYPE_ALL, CONTENT_TYPE_COMMENTS):
        row_sets.append(_comment_rows(project, state))
    if content_type in (CONTENT_TYPE_ALL, CONTENT_TYPE_ITEMS):
        for model in get_item_models():
            row_sets.append(_item_rows(model, project, state))

    if not row_sets:
        return Comment.objects.none()

    rows = row_sets[0]
    if len(row_sets) > 1:
        rows = rows.union(*row_sets[1:], all=True)

    if ordering == ORDERING_OLDEST:
        return rows.order_by("created", "pk")
    return rows.order_by("-created", "-pk")


def _related_fields(model):
    related = ["creator", "module__project"]
    field_names = {field.name for field in model._meta.get_fields()}
    if "moderator_feedback_text" in field_names:
        related.append("moderator_feedback_text")
    return related


def resolve_moderation_items(rows):
    """Load the objects referenced by moderation rows in bulk."""
    rows = list(rows)
    pks_by_type = defaultdict(list)
    for row in rows:
        pks_by_type[row["item_type"]].append(row["pk"])

    objects = {}
    comment_label = Comment._meta.label_lower
    if pks_by_type.get(comment_label):
        comments = Comment.objects.filter(pk__in=pks_by_type[comment_label])
        related = ["creator", "content_type"]
        for comment in comments.select_related(*related):
            objects[(comment_label, comment.pk)] = comment

    for model in get_item_models():
        label = model._meta.label_lower
        pks = pks_by_type.get(label)
        if not pks:
            continue
        items = model.objects.filter(pk__in=pks).select_related(*_related_fields(model))
        for item in items:
            objects[(label, item.pk)] = item

    items = [
        objects[(row["item_type"], row["pk"])]
        for row in rows
        if (row["item_type"], row["pk"]) in objects
    ]
    return attach_report_counts(items)


def _item_label(item):
    name = item.__class__.__name__
    return re.sub(r"(?<!^)(?=[A-Z])", " ", name)


def _creator_name(item):
    if isinstance(item, Comment) and (item.is_removed or item.is_censored):
        return _("unknown user")
    if not item.creator_id:
        return _("unknown user")
    return item.creator.get_short_name()


def _moderator_status(item):
    display = getattr(item, "get_moderator_status_display", None)
    if callable(display):
        try:
            return display()
        except (AttributeError, IndexError):
            return ""
    status = getattr(item, "moderator_status", "")
    return status or ""


def _moderator_feedback(item):
    feedback = getattr(item, "moderator_feedback_text", None)
    if feedback is None:
        return ""
    return getattr(feedback, "feedback_text", "") or ""


def _shorten(text):
    text = text or ""
    short_text = Truncator(text).chars(TRUNCATE_LENGTH, html=True)
    return short_text, short_text != text


def build_moderation_item(item):
    """Create the template representation of a comment or item."""
    is_comment = isinstance(item, Comment)
    if is_comment:
        title = ""
        text = transforms.clean_html_all(item.comment)
        detail_url = item.get_absolute_url()
        status = ""
        feedback = ""
        is_blocked = item.is_blocked
        is_highlighted = item.is_moderator_marked
        image = None
    else:
        title = getattr(item, "name", "")
        text = transforms.clean_html_field(getattr(item, "description", ""))
        detail_url = item.get_absolute_url()
        status = _moderator_status(item)
        feedback = transforms.clean_html_field(_moderator_feedback(item))
        is_blocked = False
        is_highlighted = False
        image = getattr(item, "image", None)

    short_text, is_truncated = _shorten(text)

    image_width = getattr(image, "width", None) if image else None
    image_height = getattr(image, "height", None) if image else None
    image_thumb_width = 330 if image_width else None
    image_thumb_height = (
        round(image_thumb_width * image_height / image_width)
        if image_width and image_height
        else image_height
    )

    return {
        "pk": item.pk,
        "key": "{}-{}".format(item._meta.label_lower.replace(".", "_"), item.pk),
        "type": item._meta.label_lower,
        "label": _("Comment") if is_comment else _item_label(item),
        "title": title,
        "author": _creator_name(item),
        "created": item.created,
        "modified": item.modified,
        "text": text,
        "short_text": short_text,
        "is_truncated": is_truncated,
        "image": image,
        "image_width": image_width,
        "image_height": image_height,
        "image_thumb_width": image_thumb_width,
        "image_thumb_height": image_thumb_height,
        "status": status,
        "status_value": (getattr(item, "moderator_status", "") or "").lower(),
        "is_comment": is_comment,
        "feedback": feedback,
        "num_reports": getattr(item, "_report_count", 0),
        "is_reviewed": bool(getattr(item, "is_reviewed", False)),
        "is_resolved": bool(getattr(item, "is_resolved", False)),
        "resolved_at": getattr(item, "resolved_at", None),
        "is_blocked": is_blocked,
        "is_hidden": is_blocked,
        "is_highlighted": is_highlighted,
        "detail_url": detail_url,
        "can_edit": True,
        "can_hide": is_comment,
        "can_edit_feedback": supports_feedback(item),
    }


def get_report_count(project):
    """Return the number of reports for comments and items of a project."""
    total = 0
    comment_ct = ContentType.objects.get_for_model(Comment)
    total += Report.objects.filter(
        content_type=comment_ct,
        object_pk__in=Comment.objects.filter(project=project).values("pk"),
    ).count()
    for model in get_item_models():
        content_type = ContentType.objects.get_for_model(model)
        total += Report.objects.filter(
            content_type=content_type,
            object_pk__in=model.objects.filter(module__project=project).values("pk"),
        ).count()
    return total


def attach_report_counts(objects):
    """Attach the number of reports to each object as ``_report_count``."""
    objects = list(objects)
    by_model = defaultdict(list)
    for obj in objects:
        obj._report_count = 0
        by_model[type(obj)].append(obj)

    for model, model_objects in by_model.items():
        content_type = ContentType.objects.get_for_model(model)
        counts = dict(
            Report.objects.filter(
                content_type=content_type,
                object_pk__in=[obj.pk for obj in model_objects],
            )
            .values_list("object_pk")
            .annotate(report_count=Count("pk"))
        )
        for obj in model_objects:
            obj._report_count = counts.get(obj.pk, 0)

    return objects


def get_moderation_item(project, item_type, pk):
    """Return a comment or item of the project or raise Http404."""
    from django.http import Http404

    if item_type == Comment._meta.label_lower:
        try:
            return Comment.objects.get(pk=pk, project=project)
        except Comment.DoesNotExist:
            raise Http404

    for model in get_item_models():
        if model._meta.label_lower != item_type:
            continue
        try:
            return model.objects.get(pk=pk, module__project=project)
        except model.DoesNotExist:
            raise Http404

    raise Http404
