import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlencode
from django.utils.translation import gettext as _
from django.views import View
from django.views import generic

from adhocracy4.projects.models import Project
from adhocracy4.rules import mixins as rules_mixins

from . import forms
from . import signals
from . import utils


def get_moderation_state(request):
    state = request.GET.get("state") or request.POST.get("state", utils.STATE_ALL)
    return state if state in utils.STATES else utils.STATE_ALL


def get_moderation_counts(project, content_type, ordering):
    return {
        filter_state: utils.get_moderation_queryset(
            project, content_type, filter_state, ordering
        ).count()
        for filter_state in (
            utils.STATE_ALL,
            utils.STATE_UNREAD,
            utils.STATE_RESOLVED,
        )
    }


class ModerationProjectMixin(LoginRequiredMixin):
    project_url_kwarg = "project_pk"

    @property
    def project(self):
        if not hasattr(self, "_project"):
            self._project = get_object_or_404(
                Project, pk=self.kwargs[self.project_url_kwarg]
            )
        return self._project

    def get_permission_object(self):
        return self.project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project"] = self.project
        context["moderation_dashboard_url"] = reverse("a4moderation:dashboard")
        return context

    def project_redirect_url(self, request):
        url = reverse("a4moderation:project", kwargs={"project_pk": self.project.pk})
        params = {
            name: request.POST.get(name)
            for name in ("state", "content_type", "ordering", "page")
            if request.POST.get(name)
        }
        if params:
            return "{}?{}".format(url, urlencode(params))
        return url

    def render_item(self, request, item):
        state = get_moderation_state(request)
        content_type = request.POST.get(
            "content_type",
            request.GET.get("content_type", utils.CONTENT_TYPE_ALL),
        )
        ordering = request.POST.get(
            "ordering", request.GET.get("ordering", utils.ORDERING_NEWEST)
        )
        return render(
            request,
            "a4moderation/includes/moderation_item.html",
            {
                "item": utils.build_moderation_item(item),
                "state": state,
                "project": self.project,
                "content_type": content_type,
                "ordering": ordering,
            },
        )


class ModerationDashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = "a4moderation/moderation_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q", "").strip()
        sort = self.request.GET.get("sort", "reports")
        projects = list(utils.get_moderated_projects(self.request.user))

        if query:
            projects = [
                project
                for project in projects
                if query.lower() in project.name.lower()
                or query.lower() in project.organisation.name.lower()
            ]
        if sort == "name":
            projects.sort(key=lambda project: project.name.lower())
        elif sort == "recent":
            projects.sort(key=lambda project: project.created, reverse=True)

        now = timezone.now()
        for project in projects:
            project.unread_count = utils.get_moderation_queryset(
                project, utils.CONTENT_TYPE_ALL, utils.STATE_UNREAD
            ).count()
            project.total_count = utils.get_moderation_queryset(
                project, utils.CONTENT_TYPE_ALL, utils.STATE_ALL
            ).count()
            project.resolved_count = utils.get_moderation_queryset(
                project, utils.CONTENT_TYPE_ALL, utils.STATE_RESOLVED
            ).count()
            project.open_count = project.total_count - project.resolved_count
            project.report_count, project.last_report_at = utils.get_report_stats(
                project
            )
            phase = project.active_phase_ends_next
            project.remaining_days = (
                max((phase.end_date - now).days, 0) if phase else None
            )

        if sort == "reports":
            projects.sort(
                key=lambda project: (
                    project.last_report_at is not None,
                    project.last_report_at,
                ),
                reverse=True,
            )

        context.update(
            {
                "moderated_projects": projects,
                "query": query,
                "sort": sort,
            }
        )
        return context


class ModerationProjectView(
    ModerationProjectMixin, rules_mixins.PermissionRequiredMixin, generic.TemplateView
):
    template_name = "a4moderation/moderation_project.html"
    permission_required = "a4moderation.moderate_project"
    paginate_by = 20

    def _get_choice(self, name, choices, default):
        value = self.request.GET.get(name, default)
        return value if value in choices else default

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        state = self._get_choice("state", utils.STATES, utils.STATE_ALL)
        content_type = self._get_choice(
            "content_type", utils.CONTENT_TYPES, utils.CONTENT_TYPE_ALL
        )
        ordering = self._get_choice("ordering", utils.ORDERINGS, utils.ORDERING_NEWEST)

        queryset = utils.get_moderation_queryset(
            self.project, content_type, state, ordering
        )
        paginator = Paginator(queryset, self.paginate_by)
        page_obj = paginator.get_page(self.request.GET.get("page"))

        counts = get_moderation_counts(self.project, content_type, ordering)

        context.update(
            {
                "state": state,
                "content_type": content_type,
                "ordering": ordering,
                "page_obj": page_obj,
                "is_paginated": page_obj.has_other_pages(),
                "counts": counts,
                "items": [
                    utils.build_moderation_item(item)
                    for item in utils.resolve_moderation_items(page_obj.object_list)
                ],
            }
        )
        return context

    def get_template_names(self):
        if self.request.headers.get("HX-Request") == "true":
            return ["a4moderation/includes/moderation_items.html"]
        return [self.template_name]


class ModerationItemMarkReadView(
    ModerationProjectMixin, rules_mixins.PermissionRequiredMixin, View
):
    permission_required = "a4moderation.moderate_project"
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        item = utils.get_moderation_item(
            self.project, kwargs["item_type"], kwargs["pk"]
        )
        is_read = request.POST.get("read", "1") != "0"
        item.is_reviewed = is_read
        item.save(ignore_modified=True, update_fields=["is_reviewed"])

        message = _("Marked as read") if is_read else _("Marked as unread")
        state = get_moderation_state(request)
        if request.headers.get("HX-Request") == "true":
            is_visible = (
                state == utils.STATE_ALL
                or (state == utils.STATE_UNREAD and not is_read)
                or (state == utils.STATE_READ and is_read)
            )
            if is_visible:
                response = render(
                    request,
                    "a4moderation/includes/moderation_item.html",
                    {
                        "item": utils.build_moderation_item(item),
                        "state": state,
                        "content_type": request.POST.get(
                            "content_type", utils.CONTENT_TYPE_ALL
                        ),
                        "ordering": request.POST.get("ordering", utils.ORDERING_NEWEST),
                        "project": self.project,
                    },
                )
            else:
                response = HttpResponse(status=200)
        else:
            response = HttpResponseRedirect(self.project_redirect_url(request))

        response["HX-Trigger"] = json.dumps(
            {
                "moderationItemUpdated": {"message": str(message)},
                "moderationCountsChanged": {},
            }
        )
        return response


class ModerationItemFeedbackView(
    ModerationProjectMixin, rules_mixins.PermissionRequiredMixin, View
):
    """Edit the status and official feedback of an item."""

    permission_required = "a4moderation.moderate_project"

    def _get_item(self, kwargs):
        item = utils.get_moderation_item(
            self.project, kwargs["item_type"], kwargs["pk"]
        )
        if not utils.supports_feedback(item):
            raise Http404
        return item

    def _get_form(self, item, data=None):
        return forms.ModerationItemFeedbackForm(data=data, item=item)

    def _context(self, item, form, is_dialog, state=utils.STATE_ALL):
        return {
            "project": self.project,
            "item": utils.build_moderation_item(item),
            "form": form,
            "is_dialog": is_dialog,
            "state": state,
            "content_type": self.request.POST.get(
                "content_type",
                self.request.GET.get("content_type", utils.CONTENT_TYPE_ALL),
            ),
            "ordering": self.request.POST.get(
                "ordering",
                self.request.GET.get("ordering", utils.ORDERING_NEWEST),
            ),
        }

    def _render_form(self, request, item, form, state, is_htmx):
        template = (
            "a4moderation/includes/feedback_form.html"
            if is_htmx
            else "a4moderation/feedback_form.html"
        )
        return render(
            request,
            template,
            self._context(item, form, is_dialog=is_htmx, state=state),
        )

    def get(self, request, *args, **kwargs):
        item = self._get_item(kwargs)
        state = get_moderation_state(request)
        form = self._get_form(item)
        is_htmx = request.headers.get("HX-Request") == "true"
        return self._render_form(request, item, form, state, is_htmx)

    def post(self, request, *args, **kwargs):
        item = self._get_item(kwargs)
        state = get_moderation_state(request)
        form = self._get_form(item, data=request.POST)
        is_htmx = request.headers.get("HX-Request") == "true"

        if form.is_valid():
            form.save(request.user)
            if form.changed:
                signals.moderation_item_feedback_saved.send(
                    sender=self.__class__, item=item, user=request.user
                )
            if not is_htmx:
                return redirect(self.project_redirect_url(request))

            item_context = utils.build_moderation_item(item)
            item_id = "moderation-item-{}".format(item_context["key"])
            if state == utils.STATE_UNREAD:
                response = HttpResponse(status=200)
            else:
                response = render(
                    request,
                    "a4moderation/includes/moderation_item.html",
                    {
                        "item": item_context,
                        "state": state,
                        "project": self.project,
                        "content_type": self.request.POST.get(
                            "content_type", utils.CONTENT_TYPE_ALL
                        ),
                        "ordering": self.request.POST.get(
                            "ordering", utils.ORDERING_NEWEST
                        ),
                    },
                )
            response["HX-Retarget"] = "#{}".format(item_id)
            response["HX-Reswap"] = "outerHTML"
            response["HX-Trigger"] = json.dumps(
                {
                    "moderationFeedbackSaved": {
                        "message": str(_("Feedback saved")),
                        "itemId": item_id,
                    },
                    "moderationCountsChanged": {},
                }
            )
            return response

        return self._render_form(request, item, form, state, is_htmx)


class ModerationItemResolveView(
    ModerationProjectMixin, rules_mixins.PermissionRequiredMixin, View
):
    permission_required = "a4moderation.moderate_project"
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        item = utils.get_moderation_item(
            self.project, kwargs["item_type"], kwargs["pk"]
        )
        resolved = request.POST.get("resolved", "1") != "0"
        item.is_resolved = resolved
        item.resolved_at = timezone.now() if resolved else None
        item.is_reviewed = True
        item.save(
            ignore_modified=True,
            update_fields=["is_resolved", "resolved_at", "is_reviewed"],
        )
        response = self.render_item(request, item)
        response["HX-Trigger"] = json.dumps(
            {
                "moderationItemUpdated": {
                    "message": str(
                        _("Marked as resolved") if resolved else _("Reopened")
                    )
                },
                "moderationCountsChanged": {},
            }
        )
        return response


class ModerationItemDeleteView(
    ModerationProjectMixin, rules_mixins.PermissionRequiredMixin, View
):
    permission_required = "a4moderation.moderate_project"
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        item = utils.get_moderation_item(
            self.project, kwargs["item_type"], kwargs["pk"]
        )
        if not utils.is_comment_item(item):
            raise Http404
        item.is_censored = True
        item.is_reviewed = True
        item.save()
        response = self.render_item(request, item)
        response["HX-Trigger"] = json.dumps(
            {
                "moderationItemUpdated": {"message": str(_("Deleted"))},
                "moderationCountsChanged": {},
            }
        )
        return response


class ModerationItemEditView(
    ModerationProjectMixin, rules_mixins.PermissionRequiredMixin, View
):
    permission_required = "a4moderation.moderate_project"

    def _get_item(self, kwargs):
        return utils.get_moderation_item(
            self.project, kwargs["item_type"], kwargs["pk"]
        )

    def _get_form(self, item, data=None):
        if utils.is_comment_item(item):
            return forms.ModerationCommentEditForm(data=data, item=item)
        return forms.ModerationItemFeedbackForm(data=data, item=item)

    def get(self, request, *args, **kwargs):
        item = self._get_item(kwargs)
        form = self._get_form(item)
        state = get_moderation_state(request)
        return render(
            request,
            "a4moderation/includes/moderation_item.html",
            {
                "item": utils.build_moderation_item(item),
                "form": form,
                "edit_mode": True,
                "state": state,
                "project": self.project,
                "content_type": request.GET.get("content_type", utils.CONTENT_TYPE_ALL),
                "ordering": request.GET.get("ordering", utils.ORDERING_NEWEST),
            },
        )

    def post(self, request, *args, **kwargs):
        item = self._get_item(kwargs)
        form = self._get_form(item, data=request.POST)
        if form.is_valid():
            form.save(request.user) if not utils.is_comment_item(item) else form.save()
            if not utils.is_comment_item(item) and form.changed:
                signals.moderation_item_feedback_saved.send(
                    sender=self.__class__, item=item, user=request.user
                )
            response = self.render_item(request, item)
            response["HX-Trigger"] = json.dumps(
                {
                    "moderationItemUpdated": {"message": str(_("Saved"))},
                    "moderationCountsChanged": {},
                }
            )
            return response
        return render(
            request,
            "a4moderation/includes/moderation_item.html",
            {
                "item": utils.build_moderation_item(item),
                "form": form,
                "edit_mode": True,
                "state": get_moderation_state(request),
                "project": self.project,
                "content_type": request.POST.get(
                    "content_type", utils.CONTENT_TYPE_ALL
                ),
                "ordering": request.POST.get("ordering", utils.ORDERING_NEWEST),
            },
        )


class ModerationCountsView(
    ModerationProjectMixin, rules_mixins.PermissionRequiredMixin, generic.TemplateView
):
    template_name = "a4moderation/includes/moderation_tabs.html"
    permission_required = "a4moderation.moderate_project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        state = get_moderation_state(self.request)
        content_type = self.request.GET.get("content_type", utils.CONTENT_TYPE_ALL)
        ordering = self.request.GET.get("ordering", utils.ORDERING_NEWEST)
        context.update(
            {
                "state": state,
                "content_type": content_type,
                "ordering": ordering,
                "counts": get_moderation_counts(self.project, content_type, ordering),
            }
        )
        return context
