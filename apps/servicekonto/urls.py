from django.conf.urls import url

from . import views

urlpatterns = [
    url('^servicekonto/login/$',
        views.login,
        name='servicekonto_login'),
    url('^servicekonto/login/redirect/$',
        views.login_redirect,
        name='servicekonto_login_redirect'),
    url('^servicekonto/callback/$',
        views.callback,
        name='servicekonto_callback'),
]
