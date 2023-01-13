from django.urls import re_path

from . import views

urlpatterns = [
    re_path(
        r"^(?P<year>\d{4})-(?P<pk>\d+)/$",
        views.IdeaDetailView.as_view(),
        name="idea-detail",
    ),
    re_path(
        r"^(?P<slug>[-\w_]+)/$", views.IdeaDetailView.as_view(), name="idea-redirect"
    ),
    re_path(
        r"create/module/(?P<module_slug>[-\w_]+)/$",
        views.IdeaCreateView.as_view(),
        name="idea-create",
    ),
    re_path(
        r"^(?P<year>\d{4})-(?P<pk>\d+)/update/$",
        views.IdeaUpdateView.as_view(),
        name="idea-update",
    ),
    re_path(
        r"^(?P<year>\d{4})-(?P<pk>\d+)/delete/$",
        views.IdeaDeleteView.as_view(),
        name="idea-delete",
    ),
    re_path(
        r"^(?P<year>\d{4})-(?P<pk>\d+)/moderate/$",
        views.IdeaModerateView.as_view(),
        name="idea-moderate",
    ),
]
