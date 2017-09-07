from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<slug>[-\w_]+)/$',
        views.MapTopicDetailView.as_view(), name='maptopic-detail'),
]
