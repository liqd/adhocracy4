from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<year>\d{4})-(?P<pk>\d+)/$',
        views.TopicDetailView.as_view(), name='topic-detail'),
    url(r'^(?P<slug>[-\w_]+)/$',
        views.TopicDetailView.as_view(), name='topic-redirect'),
    url(r'^(?P<year>\d{4})-(?P<pk>\d+)/moderate/$',
        views.TopicModerateView.as_view(), name='topic-moderate'),
]
