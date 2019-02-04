from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^vorhaben/(?P<year>\d{4})-(?P<pk>\d+)/$',
        views.PlanDetailView.as_view(), name='plan-detail'),
    url('^projekte/$',
        views.PlanListView.as_view(), name='plan-list'),
]
