from django.urls import path
from django.urls import re_path

from . import views

urlpatterns = [
    re_path(
        r"^projects/(?P<slug>[-\w_]+)/$",
        views.EmbedProjectView.as_view(),
        name="embed-project",
    ),
    path("login_success", views.EmbedLoginClose.as_view(), name="embed-login-success"),
]
