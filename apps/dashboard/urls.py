from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^(?P<organisation_slug>[-\w_]+)/projects/$',
        views.DashboardProjectListView.as_view(),
        name='dashboard-project-list'),
    url(r'^(?P<organisation_slug>[-\w_]+)/blueprints/$',
        views.DashboardBlueprintListView.as_view(),
        name='dashboard-blueprint-list'),
    url(r'^(?P<organisation_slug>[-\w_]+)/blueprints/'
        r'(?P<blueprint_slug>[-\w_]+)/$',
        views.DashboardProjectCreateView.as_view(),
        name='dashboard-project-create'),
    url(
        r'^(?P<organisation_slug>[-\w_]+)/projects/(?P<slug>[-\w_]+)/$',
        views.DashboardProjectUpdateView.as_view(),
        name='dashboard-project-edit'
    ),
]
