from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^projects/(?P<slug>[-\w_]+)/$', views.EmbedProjectView.as_view(),
        name='embed-project'),
    url('login_success', views.EmbedLoginClose.as_view(),
        name='embed-login-success'),
]
