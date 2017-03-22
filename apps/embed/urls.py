from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^projects/(?P<slug>[-\w_]+)/$', views.EmbedView.as_view(),
        name='embed-project'),
]
