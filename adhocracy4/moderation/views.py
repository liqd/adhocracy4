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
from django.utils.translation import gettext as _
from django.views import View
from django.views import generic

from adhocracy4.projects.models import Project
from adhocracy4.rules import mixins as rules_mixins

from . import forms
from . import utils


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


class ModerationDashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = "a4moderation/moderation_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["moderated_projects"] = utils.get_moderated_projects(self.request.user)
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
        state = self._get_choice("state", utils.STATES, utils.STATE_UNREAD)
        content_type = self._get_choice(
            "content_type", utils.CONTENT_TYPES, utils.CONTENT_TYPE_ALL
        )
        ordering = self._get_choice("ordering", utils.ORDERINGS, utils.ORDERING_NEWEST)

        queryset = utils.get_moderation_queryset(
            self.project, content_type, state, ordering
        )
        paginator = Paginator(queryset, self.paginate_by)
        page_obj = paginator.get_page(self.request.GET.get("page"))

        context.update(
            {
                "state": state,
                "content_type": content_type,
                "ordering": ordering,
                "page_obj": page_obj,
                "is_paginated": page_obj.has_other_pages(),
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
        if request.headers.get("HX-Request") == "true":
            state = request.POST.get("state", utils.STATE_ALL)
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
                        "project": self.project,
                    },
                )
            else:
                response = HttpResponse(status=200)
        else:
            response = HttpResponseRedirect(
                reverse("a4moderation:project", kwargs={"project_pk": self.project.pk})
            )

        response["HX-Trigger"] = json.dumps(
            {"moderationItemUpdated": {"message": str(message)}}
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

    @staticmethod
    def _get_state(request):
        state = request.GET.get("state") or request.POST.get("state", utils.STATE_ALL)
        return state if state in utils.STATES else utils.STATE_ALL

    def _context(self, item, form, is_dialog, state=utils.STATE_ALL):
        return {
            "project": self.project,
            "item": utils.build_moderation_item(item),
            "form": form,
            "is_dialog": is_dialog,
            "state": state,
        }

    def get(self, request, *args, **kwargs):
        item = self._get_item(kwargs)
        state = self._get_state(request)
        form = self._get_form(item)
        is_htmx = request.headers.get("HX-Request") == "true"
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

    def post(self, request, *args, **kwargs):
        item = self._get_item(kwargs)
        state = self._get_state(request)
        form = self._get_form(item, data=request.POST)
        is_htmx = request.headers.get("HX-Request") == "true"

        if form.is_valid():
            form.save(request.user)
            if not is_htmx:
                return redirect(
                    "{}?state={}".format(
                        reverse(
                            "a4moderation:project",
                            kwargs={"project_pk": self.project.pk},
                        ),
                        state,
                    )
                )

            item_context = utils.build_moderation_item(item)
            response = render(
                request,
                "a4moderation/includes/moderation_item.html",
                {"item": item_context, "state": state, "project": self.project},
            )
            response["HX-Retarget"] = "#moderation-item-{}".format(item_context["key"])
            response["HX-Reswap"] = "outerHTML"
            response["HX-Trigger"] = json.dumps(
                {
                    "moderationFeedbackSaved": {
                        "message": str(_("Feedback saved")),
                        "itemId": "moderation-item-{}".format(item_context["key"]),
                    }
                }
            )
            return response

        template = (
            "a4moderation/includes/feedback_form.html"
            if is_htmx
            else "a4moderation/feedback_form.html"
        )
        return render(
            request,
            template,
            self._context(
                item,
                form,
                is_dialog=is_htmx,
                state=state,
            ),
        )
