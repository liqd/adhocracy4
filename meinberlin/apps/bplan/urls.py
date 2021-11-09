from django.urls import path

from . import views

urlpatterns = [
    path('sent/', views.BplanStatementSentView.as_view(),
         name='statement-sent'),
    path('finished/', views.BplanFinishedView.as_view(),
         name='finished'),
]
