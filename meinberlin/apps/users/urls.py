from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<slug>[-\w _.@+-]+)/$', views.ProfileView.as_view(),
        name='profile'),
]
