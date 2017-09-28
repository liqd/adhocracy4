from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^sent/$', views.BplanStatementSentView.as_view(),
        name='statement-sent'),
    url(r'^finished/$', views.BplanFinishedView.as_view(),
        name='finished'),
]
