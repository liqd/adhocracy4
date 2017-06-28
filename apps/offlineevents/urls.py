from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<slug>[-\w_]+)/$',
        views.OfflineEventDetailView.as_view(), name='offlineevent-detail'),
    url(r'^/manage/projects/(?P<slug>[-\w_]+)/$',
        views.OfflineEventListView.as_view(), name='offlineevent-list'),
    url(r'^manage/create/project/(?P<slug>[-\w_]+)/$',
        views.OfflineEventCreateView.as_view(),
        name='offlineevent-create'),
    url(r'^manage/(?P<slug>[-\w_]+)/update/$',
        views.OfflineEventUpdateView.as_view(),
        name='offlineevent-update'),
    url(r'^manage/(?P<slug>[-\w_]+)/delete/$',
        views.OfflineEventDeleteView.as_view(),
        name='offlineevent-delete'),
]
