from django.urls import re_path

from . import views

urlpatterns = [
    re_path(
        r"^(?P<slug>[-\w_]+)/$",
        views.OfflineEventDetailView.as_view(),
        name="offlineevent-detail",
    ),
]
