from django.urls import re_path

from . import views

urlpatterns = [
    re_path(
        r"^(?P<slug>[-\w_]+)/$",
        views.ProjectDetailView.as_view(),
        name="project-detail",
    ),
]
