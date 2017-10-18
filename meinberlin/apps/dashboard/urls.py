from django.conf.urls import url

from meinberlin.apps.bplan.views import BplanProjectCreateView
from meinberlin.apps.dashboard2.urls import \
    urlpatterns as a4dashboard_urlpatterns
from meinberlin.apps.extprojects.views import ExternalProjectCreateView
from meinberlin.apps.projectcontainers.views import ContainerCreateView
from meinberlin.apps.projectcontainers.views import ContainerListView
from meinberlin.apps.projects.views import DashboardProjectListView

from . import views

app_name = 'a4dashboard'

urlpatterns = [
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/settings/$',
        views.DashboardOrganisationUpdateView.as_view(),
        name='organisation-edit'),
    url(r'^newsletters/(?P<organisation_slug>[-\w_]+)/create/$',
        views.DashboardNewsletterCreateView.as_view(),
        name='newsletter-create'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/containers/$',
        ContainerListView.as_view(),
        name='container-list'),

    # Overwrite the ProjectUpdateView with meinBerlin urls
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/blueprints/'
        r'external-project/$',
        ExternalProjectCreateView.as_view(),
        name='external-project-create'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/blueprints/'
        r'bplan/$',
        BplanProjectCreateView.as_view(),
        name='bplan-project-create'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/blueprints/'
        r'container/$',
        ContainerCreateView.as_view(),
        name='container-create'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/projects/$',
        DashboardProjectListView.as_view(),
        name='project-list'),
] + a4dashboard_urlpatterns
