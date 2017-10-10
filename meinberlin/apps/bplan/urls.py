from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^sent/$', views.BplanStatemenSentView.as_view(),
        name='statement-sent'),
    url(r'^finished/$', views.BplanFinishedView.as_view(),
        name='finished'),
]
