from django.conf.urls import url

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
    url(r'^projects/(?P<project_slug>[-\w_]+)/'
        r'(?P<component_identifier>[-_:\w]+)/$',
        views.ProjectComponentDispatcher.as_view(),
        name='project-edit-component'),
    url(r'^modules/(?P<module_slug>[-\w_]+)/'
        r'(?P<component_identifier>[-_:\w]+)/$',
        views.ModuleComponentDispatcher.as_view(),
        name='module-edit-component'),
    url(r'^publish/project/(?P<project_slug>[-\w_]+)/$',
        views.ProjectPublishView.as_view(),
        name='project-publish'),
]
