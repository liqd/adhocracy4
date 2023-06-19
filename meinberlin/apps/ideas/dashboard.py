from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from adhocracy4.dashboard import DashboardComponent
from adhocracy4.dashboard import components

from . import exports
from . import views


class ExportIdeaComponent(DashboardComponent):
    identifier = "idea_export"
    weight = 50
    label = _("Export Excel")

    def is_effective(self, module):
        return (
            module.blueprint_type in ["IC", "BS"]
            and not module.project.is_draft
            and not module.is_draft
        )

    def get_progress(self, module):
        return 0, 0

    def get_base_url(self, module):
        return reverse(
            "a4dashboard:idea-export-module",
            kwargs={
                "module_slug": module.slug,
            },
        )

    def get_urls(self):
        return [
            (
                r"^modules/(?P<module_slug>[-\w_]+)/export/idea/$",
                views.IdeaDashboardExportView.as_view(component=self),
                "idea-export-module",
            ),
            (
                r"^modules/(?P<module_slug>[-\w_]+)/export/idea/ideas/$",
                exports.IdeaExportView.as_view(),
                "idea-export",
            ),
            (
                r"^modules/(?P<module_slug>[-\w_]+)/export/idea/comments/$",
                exports.IdeaCommentExportView.as_view(),
                "idea-comment-export",
            ),
        ]


class ModuleCategoriesComponent(DashboardComponent):
    identifier = "categories"
    weight = 13
    label = _("Categories")

    def is_effective(self, module):
        module_app = module.phases[0].content().app
        for app, name in settings.A4_CATEGORIZABLE:
            if app == module_app:
                return True
        return False

    def get_base_url(self, module):
        return reverse(
            "a4dashboard:dashboard-categories-edit",
            kwargs={"module_slug": module.slug},
        )

    def get_urls(self):
        return [
            (
                r"^modules/(?P<module_slug>[-\w_]+)/categories/$",
                views.DashboardCategoriesWithAliasView.as_view(component=self),
                "dashboard-categories-edit",
            )
        ]


class ModuleLabelsComponent(DashboardComponent):
    identifier = "labels"
    weight = 14
    label = _("Labels")

    def is_effective(self, module):
        module_app = module.phases[0].content().app
        for app, name in settings.A4_LABELS_ADDABLE:
            if app == module_app:
                return True
        return False

    def get_base_url(self, module):
        return reverse(
            "a4dashboard:dashboard-labels-edit",
            kwargs={"module_slug": module.slug},
        )

    def get_urls(self):
        return [
            (
                r"^modules/(?P<module_slug>[-\w_]+)/labels/$",
                views.DashboardLabelsWithAliasView.as_view(component=self),
                "dashboard-labels-edit",
            )
        ]


components.register_module(ExportIdeaComponent())
components.replace_module(ModuleCategoriesComponent())
components.replace_module(ModuleLabelsComponent())
