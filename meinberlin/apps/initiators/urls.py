from django.urls import path

from . import views

urlpatterns = [
    path('request/',
         views.InitiatorRequestView.as_view(),
         name='initiator_request'),
]
