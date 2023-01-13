from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from adhocracy4.dashboard import DashboardComponent
from adhocracy4.dashboard import components

from . import exports
from . import models
from . import views


class TopicEditComponent(DashboardComponent):
    identifier = "topic_edit"
    weight = 20
    label = _("Topics")

    def is_effective(self, module):
        return module.blueprint_type == "TP"

    def get_progress(self, module):
        if models.Topic.objects.filter(module=module).exists():
            return 1, 1
        return 0, 1

    def get_base_url(self, module):
        return reverse("a4dashboard:topic-list", kwargs={"module_slug": module.slug})

    def get_urls(self):
        return [
            (
                r"^topics/module/(?P<module_slug>[-\w_]+)/$",
                views.TopicListDashboardView.as_view(component=self),
                "topic-list",
            ),
            (
                r"^topics/create/module/(?P<module_slug>[-\w_]+)/$",
                views.TopicCreateView.as_view(component=self),
                "topic-create",
            ),
            (
                r"^topics/(?P<year>\d{4})-(?P<pk>\d+)/update/$",
                views.TopicUpdateView.as_view(component=self),
                "topic-update",
            ),
            (
                r"^topics/(?P<year>\d{4})-(?P<pk>\d+)/delete/$",
                views.TopicDeleteView.as_view(component=self),
                "topic-delete",
            ),
        ]


components.register_module(TopicEditComponent())


class ExportTopicComponent(DashboardComponent):
    identifier = "topic_export"
    weight = 50
    label = _("Export Excel")

    def is_effective(self, module):
        return (
            module.blueprint_type == "TP"
            and not module.project.is_draft
            and not module.is_draft
        )

    def get_progress(self, module):
        return 0, 0

    def get_base_url(self, module):
        return reverse(
            "a4dashboard:topic-export-module",
            kwargs={
                "module_slug": module.slug,
            },
        )

    def get_urls(self):
        return [
            (
                r"^modules/(?P<module_slug>[-\w_]+)/export/topic/$",
                views.TopicDashboardExportView.as_view(component=self),
                "topic-export-module",
            ),
            (
                r"^modules/(?P<module_slug>[-\w_]+)/export/topic/maptopics/$",
                exports.TopicExportView.as_view(),
                "topic-export",
            ),
            (
                r"^modules/(?P<module_slug>[-\w_]+)/export/topic/comments/$",
                exports.TopicCommentExportView.as_view(),
                "topic-comment-export",
            ),
        ]


components.register_module(ExportTopicComponent())
