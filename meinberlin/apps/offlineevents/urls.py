from django.conf.urls import url

from . import views
from . import views_old

urlpatterns = [
    url(r'^(?P<slug>[-\w_]+)/$',
        views.OfflineEventDetailView.as_view(), name='offlineevent-detail'),
    url(r'^projects/(?P<project_slug>[-\w_]+)/$',
        views_old.OfflineEventListView.as_view(), name='offlineevent-list'),
    url(r'^create/project/(?P<project_slug>[-\w_]+)/$',
        views_old.OfflineEventCreateView.as_view(),
        name='offlineevent-create'),
    url(r'^(?P<slug>[-\w_]+)/update/$',
        views_old.OfflineEventUpdateView.as_view(),
        name='offlineevent-update'),
    url(r'^(?P<slug>[-\w_]+)/delete/$',
        views_old.OfflineEventDeleteView.as_view(),
        name='offlineevent-delete'),
]
