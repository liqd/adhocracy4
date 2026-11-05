from django.urls import path

from . import views

app_name = "a4moderation"

urlpatterns = [
    path("", views.ModerationDashboardView.as_view(), name="dashboard"),
    path(
        "<int:project_pk>/",
        views.ModerationProjectView.as_view(),
        name="project",
    ),
    path(
        "<int:project_pk>/counts/",
        views.ModerationCountsView.as_view(),
        name="counts",
    ),
    path(
        "<int:project_pk>/items/<str:item_type>/<int:pk>/read/",
        views.ModerationItemMarkReadView.as_view(),
        name="item-read",
    ),
    path(
        "<int:project_pk>/items/<str:item_type>/<int:pk>/feedback/",
        views.ModerationItemFeedbackView.as_view(),
        name="item-feedback",
    ),
    path(
        "<int:project_pk>/items/<str:item_type>/<int:pk>/edit/",
        views.ModerationItemEditView.as_view(),
        name="item-edit",
    ),
    path(
        "<int:project_pk>/items/<str:item_type>/<int:pk>/resolve/",
        views.ModerationItemResolveView.as_view(),
        name="item-resolve",
    ),
    path(
        "<int:project_pk>/items/<str:item_type>/<int:pk>/hide/",
        views.ModerationItemHideView.as_view(),
        name="item-hide",
    ),
]
