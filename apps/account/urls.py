from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',
        views.ProfileUpdateView.as_view(),
        name='account'),
    url(r'^profile/$',
        views.ProfileUpdateView.as_view(),
        name='account-profile'),
    url(r'^change_password/$',
        views.ChangePasswordView.as_view(),
        name='account-password'),
    url(r'^email/$',
        views.DashboardEmailView.as_view(),
        name='account-email'),
]
