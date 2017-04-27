from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<slug>[-\w_]+)/$',
        views.TopicDetailView.as_view(), name='topic-detail'),
    url(r'^manage/(?P<slug>[-\w_]+)/$',
        views.TopicMgmtDetailView.as_view(), name='topic-mgmt-detail'),
    url(r'^manage/create/module/(?P<slug>[-\w_]+)/$',
        views.TopicMgmtCreateView.as_view(), name='topic-mgmt-create'),
    url(r'^manage/(?P<slug>[-\w_]+)/update/$',
        views.TopicMgmtUpdateView.as_view(), name='topic-mgmt-update'),
    url(r'^manage/(?P<slug>[-\w_]+)/delete/$',
        views.TopicMgmtDeleteView.as_view(), name='topic-mgmt-delete'),
]
