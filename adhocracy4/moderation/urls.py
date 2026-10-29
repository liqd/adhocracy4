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
        "<int:project_pk>/items/<str:item_type>/<int:pk>/read/",
        views.ModerationItemMarkReadView.as_view(),
        name="item-read",
    ),
    path(
        "<int:project_pk>/items/<str:item_type>/<int:pk>/feedback/",
        views.ModerationItemFeedbackView.as_view(),
        name="item-feedback",
    ),
]
