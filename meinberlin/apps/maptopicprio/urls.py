from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<year>\d{4})-(?P<pk>\d+)/$',
        views.MapTopicDetailView.as_view(), name='maptopic-detail'),
    url(r'^(?P<slug>[-\w_]+)/$',
        views.MapTopicDetailView.as_view(), name='maptopic-redirect'),
]
