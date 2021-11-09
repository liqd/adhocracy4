from django.urls import path
from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^vorhaben/(?P<year>\d{4})-(?P<pk>\d+)/$',
            views.PlanDetailView.as_view(), name='plan-detail'),
    path('projekte/',
         views.PlanListView.as_view(), name='plan-list'),
]
