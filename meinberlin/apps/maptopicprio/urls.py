from django.urls import re_path

from . import views

urlpatterns = [
    re_path(
        r"^(?P<year>\d{4})-(?P<pk>\d+)/$",
        views.MapTopicDetailView.as_view(),
        name="maptopic-detail",
    ),
    re_path(
        r"^(?P<slug>[-\w_]+)/$",
        views.MapTopicDetailView.as_view(),
        name="maptopic-redirect",
    ),
]
