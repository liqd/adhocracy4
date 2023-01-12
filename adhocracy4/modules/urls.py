from django.urls import re_path

from . import views

urlpatterns = [
    re_path(
        r"^(?P<module_slug>[-\w_]+)/$",
        views.ModuleDetailView.as_view(),
        name="module-detail",
    ),
]
