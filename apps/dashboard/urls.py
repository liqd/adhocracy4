from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^profile/$',
        views.DashboardProfileView.as_view(),
        name='dashboard-profile'),
    url(r'^change_password/$',
        views.ChangePasswordView.as_view(),
        name='dashboard-password'),
    url(r'^email/$',
        views.DashboardEmailView.as_view(),
        name='dashboard-email'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/settings/$',
        views.DashboardOrganisationUpdateView.as_view(),
        name='dashboard-organisation-edit'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/projects/$',
        views.DashboardProjectListView.as_view(),
        name='dashboard-project-list'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/blueprints/$',
        views.DashboardBlueprintListView.as_view(),
        name='dashboard-blueprint-list'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/blueprints/'
        r'(?P<blueprint_slug>[-\w_]+)/$',
        views.DashboardProjectCreateView.as_view(),
        name='dashboard-project-create'),
    url(r'^projects/(?P<slug>[-\w_]+)/$',
        views.DashboardProjectUpdateView.as_view(),
        name='dashboard-project-edit'),
    url(r'^projects/(?P<slug>[-\w_]+)/moderators/$',
        views.DashboardProjectModeratorsView.as_view(),
        name='dashboard-project-moderators'),
]
