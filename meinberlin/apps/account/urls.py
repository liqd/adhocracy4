from django.urls import path

from . import api
from . import views

urlpatterns = [
    path("", views.AccountView.as_view(), name="account"),
    path("profile/", views.ProfileUpdateView.as_view(), name="account_profile"),
    path("actions/", views.ProfileActionsView.as_view(), name="account_actions"),
    path("end-session/", api.EndSessionView.as_view(), name="end_session"),
]
