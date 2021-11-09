from django.urls import path

from . import views

urlpatterns = [
    path('servicekonto/login/',
         views.login,
         name='servicekonto_login'),
    path('servicekonto/login/redirect/',
         views.login_redirect,
         name='servicekonto_login_redirect'),
    path('servicekonto/callback/',
         views.callback,
         name='servicekonto_callback'),
]
