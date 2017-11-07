from django.conf.urls import include
from django.conf.urls import url

from . import components
from . import views

app_name = 'a4dashboard'
urlpatterns = [
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
    url(r'^publish/project/(?P<project_slug>[-\w_]+)/$',
        views.ProjectPublishView.as_view(),
        name='project-publish'),
    url(r'^projects/(?P<project_slug>[-\w_]+)/blueprints/$',
        views.ModuleBlueprintListView.as_view(),
        name='module-blueprint-list'),
    url(r'^projects/(?P<project_slug>[-\w_]+)/blueprints/'
        '(?P<blueprint_slug>[-\w_]+)/$',
        views.ModuleCreateView.as_view(),
        name='module-create'),
    url(r'', include(components.get_urls())),
]
