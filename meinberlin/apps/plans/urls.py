from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<slug>[-\w_]+)/$',
        views.PlanDetailView.as_view(), name='plan-detail'),
    url('',
        views.PlanListView.as_view(), name='plan-list'),
]
