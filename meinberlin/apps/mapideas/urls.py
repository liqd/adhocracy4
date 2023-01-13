from django.urls import re_path

from . import views

urlpatterns = [
    re_path(
        r"^(?P<year>\d{4})-(?P<pk>\d+)/$",
        views.MapIdeaDetailView.as_view(),
        name="mapidea-detail",
    ),
    re_path(
        r"^(?P<slug>[-\w_]+)/$",
        views.MapIdeaDetailView.as_view(),
        name="mapidea-redirect",
    ),
    re_path(
        r"create/module/(?P<module_slug>[-\w_]+)/$",
        views.MapIdeaCreateView.as_view(),
        name="mapidea-create",
    ),
    re_path(
        r"^(?P<year>\d{4})-(?P<pk>\d+)/update/$",
        views.MapIdeaUpdateView.as_view(),
        name="mapidea-update",
    ),
    re_path(
        r"^(?P<year>\d{4})-(?P<pk>\d+)/delete/$",
        views.MapIdeaDeleteView.as_view(),
        name="mapidea-delete",
    ),
    re_path(
        r"^(?P<year>\d{4})-(?P<pk>\d+)/moderate/$",
        views.MapIdeaModerateView.as_view(),
        name="mapidea-moderate",
    ),
]
