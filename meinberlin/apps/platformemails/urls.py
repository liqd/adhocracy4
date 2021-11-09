from django.urls import path

from . import views

urlpatterns = [
    path('create/',
         views.PlatformEmailCreateView.as_view(), name='create'),
]
