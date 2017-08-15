from django.conf.urls import include
from django.conf.urls import url

from . import views

app_name = 'a4dashboard'
dashboard_patterns = [
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/projects/$',
        views.ProjectListView.as_view(),
        name='project-list'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/blueprints/$',
        views.BlueprintListView.as_view(),
        name='blueprint-list'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/blueprints/'
        r'(?P<blueprint_slug>[-\w_]+)/$',
        views.ProjectCreateView.as_view(),
        name='project-create'),
    url(r'^projects/(?P<project_slug>[-\w_]+)/$',
        views.ProjectUpdateView.as_view(),
        name='project-edit'),
]

# FIXME: Pre 1.11 workaround
urlpatterns = [
    url('', include(dashboard_patterns, app_name=app_name, namespace=app_name))
]
