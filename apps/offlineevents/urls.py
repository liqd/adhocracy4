from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<slug>[-\w_]+)/$',
        views.OfflineEventDetailView.as_view(), name='offlineevent-detail'),
    url(r'^/manage/projects/(?P<slug>[-\w_]+)/$',
        views.OfflineEventMgmtView.as_view(), name='offlineevent-mgmt'),
    url(r'^manage/create/project/(?P<slug>[-\w_]+)/$',
        views.OfflineEventMgmtCreateView.as_view(),
        name='offlineevent-mgmt-create'),
    url(r'^manage/(?P<slug>[-\w_]+)/update/$',
        views.OfflineEventMgmtUpdateView.as_view(),
        name='offlineevent-mgmt-update'),
    url(r'^manage/(?P<slug>[-\w_]+)/delete/$',
        views.OfflineEventMgmtDeleteView.as_view(),
        name='offlineevent-mgmt-delete'),
]
