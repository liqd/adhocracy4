from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',
        views.AccountView.as_view(),
        name='account'),
    url(r'^profile/$',
        views.ProfileUpdateView.as_view(),
        name='account_profile'),
    url(r'^actions/$',
        views.ProfileActionsView.as_view(),
        name='account_actions'),
]
