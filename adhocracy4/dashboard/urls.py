from django.urls import include
from django.urls import path
from django.urls import re_path

from . import components
from . import views

app_name = "a4dashboard"
urlpatterns = [
    re_path(
        r"^organisations/(?P<organisation_slug>[-\w_]+)/projects/$",
        views.ProjectListView.as_view(),
        name="project-list",
    ),
    re_path(
        r"^organisations/(?P<organisation_slug>[-\w_]+)/blueprints/$",
        views.BlueprintListView.as_view(),
        name="blueprint-list",
    ),
    re_path(
        r"^organisations/(?P<organisation_slug>[-\w_]+)/blueprints/"
        r"(?P<blueprint_slug>[-\w_]+)/$",
        views.ProjectCreateView.as_view(),
        name="project-create",
    ),
    re_path(
        r"^projects/(?P<project_slug>[-\w_]+)/$",
        views.ProjectUpdateView.as_view(),
        name="project-edit",
    ),
    re_path(
        r"^publish/project/(?P<project_slug>[-\w_]+)/$",
        views.ProjectPublishView.as_view(),
        name="project-publish",
    ),
    path("", include(components.get_urls())),
]
