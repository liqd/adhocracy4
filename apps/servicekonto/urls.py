from django.conf.urls import url

from . import views

urlpatterns = [
    url('^servicekonto/login/$', views.login, name="servicekonto_login"),
    url('^servicekonto/callback/$', views.callback,
        name='servicekonto_callback'),
]
