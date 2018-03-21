from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<slug>[-\w_]+)/$',
        views.OfflineEventDetailView.as_view(), name='offlineevent-detail'),
]
