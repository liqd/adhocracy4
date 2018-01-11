from django.conf.urls import url

from meinberlin.apps.bplan.views import BplanProjectCreateView
from meinberlin.apps.dashboard2.urls import \
    urlpatterns as a4dashboard_urlpatterns
from meinberlin.apps.extprojects.views import ExternalProjectCreateView
from meinberlin.apps.newsletters import views as newsletter_views
from meinberlin.apps.organisations import views as organisation_views
from meinberlin.apps.plans import views as plan_views
from meinberlin.apps.projectcontainers import views as container_views

from . import views

app_name = 'a4dashboard'

urlpatterns = [
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/settings/$',
        organisation_views.DashboardOrganisationUpdateView.as_view(),
        name='organisation-edit'),
    url(r'^newsletters/(?P<organisation_slug>[-\w_]+)/create/$',
        newsletter_views.DashboardNewsletterCreateView.as_view(),
        name='newsletter-create'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/containers/$',
        container_views.ContainerListView.as_view(),
        name='container-list'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/plans/$',
        plan_views.DashboardPlanListView.as_view(),
        name='plan-list'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/plans/create/$',
        plan_views.DashboardPlanCreateView.as_view(),
        name='plan-create'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)'
        r'/plans/(?P<pk>\d+)/$',
        plan_views.DashboardPlanUpdateView.as_view(),
        name='plan-update'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)'
        r'/plans/(?P<pk>\d+)/delete/$',
        plan_views.DashboardPlanDeleteView.as_view(),
        name='plan-delete'),

    # Overwrite adhocracy4 core urls with meinBerlin urls
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
        container_views.ContainerCreateView.as_view(),
        name='container-create'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/projects/$',
        views.DashboardProjectListView.as_view(),
        name='project-list'),
] + a4dashboard_urlpatterns
