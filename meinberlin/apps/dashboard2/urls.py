from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/projects/$',
        views.DashboardProjectListView.as_view(),
        name='dashboard2-project-list'),
]
