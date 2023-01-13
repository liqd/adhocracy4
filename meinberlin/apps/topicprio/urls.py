from django.urls import re_path

from . import views

urlpatterns = [
    re_path(
        r"^(?P<year>\d{4})-(?P<pk>\d+)/$",
        views.TopicDetailView.as_view(),
        name="topic-detail",
    ),
    re_path(
        r"^(?P<slug>[-\w_]+)/$", views.TopicDetailView.as_view(), name="topic-redirect"
    ),
]
