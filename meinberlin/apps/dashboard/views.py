import json
from urllib import parse

from django.apps import apps
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import resolve
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.views.generic.detail import SingleObjectMixin

from adhocracy4.dashboard import get_project_dashboard
from adhocracy4.dashboard import mixins
from adhocracy4.dashboard import signals
from adhocracy4.dashboard import views as a4dashboard_views
from adhocracy4.dashboard.blueprints import get_blueprints
from adhocracy4.modules import models as module_models
from adhocracy4.phases import models as phase_models
from adhocracy4.projects import models as project_models
from adhocracy4.projects.mixins import ProjectMixin
from adhocracy4.rules.mixins import PermissionRequiredMixin
from meinberlin.apps.dashboard.forms import DashboardProjectCreateForm
from meinberlin.apps.dashboard.mixins import DashboardProjectListGroupMixin


class ModuleBlueprintListView(
    ProjectMixin, mixins.DashboardBaseMixin, mixins.BlueprintMixin, generic.DetailView
):
    template_name = "meinberlin_dashboard/module_blueprint_list_dashboard.html"
    permission_required = "a4projects.change_project"
    model = project_models.Project
    slug_url_kwarg = "project_slug"
    menu_item = "project"

    @property
    def blueprints(self):
        return get_blueprints()

    def get_permission_object(self):
        return self.project


class ModuleCreateView(
    ProjectMixin,
    mixins.DashboardBaseMixin,
    mixins.BlueprintMixin,
    SingleObjectMixin,
    generic.View,
):
    permission_required = "a4projects.change_project"
    model = project_models.Project
    slug_url_kwarg = "project_slug"
    success_message = _("The module was created")

    def post(self, request, *args, **kwargs):
        project = self.get_object()
        weight = 1
        if project.modules:
            weight = max(project.modules.values_list("weight", flat=True)) + 1
        module = module_models.Module(
            name=self.blueprint.title,
            weight=weight,
            project=project,
            is_draft=True,
            blueprint_type=self.blueprint.type,
        )
        module.save()
        signals.module_created.send(sender=None, module=module, user=self.request.user)

        self._create_module_settings(module)
        self._create_phases(module, self.blueprint.content)
        messages.success(self.request, self.success_message)

        cookie = request.COOKIES.get("dashboard_projects_closed_accordions", "[]")
        ids = json.loads(parse.unquote(cookie))
        if self.project.id not in ids:
            ids.append(self.project.id)

        cookie = parse.quote(json.dumps(ids))

        response = HttpResponseRedirect(self.get_next(module))
        response.set_cookie("dashboard_projects_closed_accordions", cookie)
        return response

    def _create_module_settings(self, module):
        if self.blueprint.settings_model:
            settings_model = apps.get_model(*self.blueprint.settings_model)
            module_settings = settings_model(module=module)
            module_settings.save()

    def _create_phases(self, module, blueprint_phases):
        for index, phase_content in enumerate(blueprint_phases):
            phase = phase_models.Phase(
                type=phase_content.identifier,
                name=phase_content.name,
                description=phase_content.description,
                weight=index,
                module=module,
            )
            phase.save()

    def get_next(self, module):
        return reverse(
            "a4dashboard:dashboard-module_basic-edit",
            kwargs={"module_slug": module.slug},
        )

    def get_permission_object(self):
        return self.project


class ModulePublishView(SingleObjectMixin, PermissionRequiredMixin, generic.View):
    permission_required = "a4projects.change_project"
    model = module_models.Module
    slug_url_kwarg = "module_slug"

    def get_permission_object(self):
        return self.get_object().project

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action", None)
        if action == "publish":
            self.publish_module()
        elif action == "unpublish":
            self.unpublish_module()
        else:
            messages.warning(self.request, _("Invalid action"))

        return HttpResponseRedirect(self.get_next())

    def get_next(self):
        if "referrer" in self.request.POST:
            return self.request.POST["referrer"]
        elif "Referer" in self.request.headers:
            return self.request.headers["Referer"]

        return reverse(
            "a4dashboard:project-edit",
            kwargs={"project_slug": self.get_object().project.slug},
        )

    def publish_module(self):
        module = self.get_object()
        if not module.is_draft:
            messages.info(self.request, _("Module is already added"))
            return

        dashboard = get_project_dashboard(module.project)
        num_valid, num_required = dashboard.get_module_progress(module)
        is_complete = num_valid == num_required

        if not is_complete:
            messages.error(
                self.request,
                _("Module cannot be added. " "Required fields are missing."),
            )
            return

        module.is_draft = False
        module.save()

        signals.module_published.send(
            sender=None, module=module, user=self.request.user
        )

        messages.success(self.request, _("The module is displayed in the project."))

    def unpublish_module(self):
        module = self.get_object()
        if module.is_draft:
            messages.info(self.request, _("Module is already removed"))
            return
        if not module.project.is_draft:
            messages.error(
                self.request, _("Module cannot be removed " "from a published project.")
            )
            return
        if module.project.published_modules.count() == 1:
            messages.error(
                self.request,
                _(
                    "Module cannot be removed. "
                    "It is the only module added to the project."
                ),
            )
            return

        module.is_draft = True
        module.save()

        signals.module_unpublished.send(
            sender=None, module=module, user=self.request.user
        )

        messages.success(
            self.request, _("The module is no longer displayed in the project.")
        )


class ModuleDeleteView(PermissionRequiredMixin, generic.DeleteView):
    permission_required = "a4projects.change_project"
    model = module_models.Module
    success_message = _("The module has been deleted")

    def form_valid(self, request, *args, **kwargs):
        if not self.get_object().is_draft:
            messages.error(
                self.request, _("Module added to a project cannot be " "deleted.")
            )
            failure_url = self.get_failure_url()
            return HttpResponseRedirect(failure_url)
        messages.success(self.request, self.success_message)
        return super().form_valid(request, *args, **kwargs)

    def get_permission_object(self):
        return self.get_object().project

    def get_success_url(self):
        referrer = self.request.POST.get("referrer", None) or self.request.headers.get(
            "Referer", None
        )
        if referrer:
            view, args, kwargs = resolve(referrer)
            if (
                "module_slug" not in kwargs
                or not kwargs["module_slug"] == self.get_object().slug
            ):
                return referrer

        return reverse(
            "a4dashboard:project-edit",
            kwargs={
                "project_slug": self.get_object().project.slug,
            },
        )

    def get_failure_url(self):
        if "referrer" in self.request.POST:
            return self.request.POST["referrer"]
        elif "Referer" in self.request.headers:
            return self.request.headers["Referer"]

        return reverse(
            "a4dashboard:project-edit",
            kwargs={
                "project_slug": self.get_object().project.slug,
            },
        )


class DashboardProjectListView(
    DashboardProjectListGroupMixin, a4dashboard_views.ProjectListView
):
    def get_queryset(self):
        return super().get_queryset().filter(externalproject=None)


class ProjectCreateView(
    mixins.DashboardBaseMixin, SuccessMessageMixin, generic.CreateView
):
    model = project_models.Project
    slug_url_kwarg = "project_slug"
    form_class = DashboardProjectCreateForm
    template_name = "a4dashboard/project_create_form.html"
    permission_required = "a4projects.add_project"
    menu_item = "project"
    success_message = _("Project was created.")

    def get_permission_object(self):
        return self.organisation

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["organisation"] = self.organisation
        kwargs["creator"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse(
            "a4dashboard:project-edit", kwargs={"project_slug": self.object.slug}
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        signals.project_created.send(
            sender=None, project=self.object, user=self.request.user
        )

        return response
