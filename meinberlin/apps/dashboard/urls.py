from django.conf.urls import url

from adhocracy4.dashboard.urls import urlpatterns as a4dashboard_urlpatterns
from meinberlin.apps.bplan import views as bplan_views
from meinberlin.apps.extprojects import views as extproject_views
from meinberlin.apps.newsletters import views as newsletter_views
from meinberlin.apps.organisations import views as organisation_views
from meinberlin.apps.plans import views as plan_views
from meinberlin.apps.plans.exports import DashboardPlanExportView
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
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/bplans/$',
        bplan_views.BplanProjectListView.as_view(),
        name='bplan-list'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/external-projects/$',
        extproject_views.ExternalProjectListView.as_view(),
        name='extproject-list'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/plans/$',
        plan_views.DashboardPlanListView.as_view(),
        name='plan-list'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/plans/create/$',
        plan_views.DashboardPlanCreateView.as_view(),
        name='plan-create'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/plans/export/$',
        DashboardPlanExportView.as_view(),
        name='plan-export'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)'
        r'/plans/(?P<pk>\d+)/$',
        plan_views.DashboardPlanUpdateView.as_view(),
        name='plan-update'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)'
        r'/plans/(?P<pk>\d+)/delete/$',
        plan_views.DashboardPlanDeleteView.as_view(),
        name='plan-delete'),
    url(r'^projects/(?P<project_slug>[-\w_]+)/blueprints/$',
        views.ModuleBlueprintListView.as_view(),
        name='module-blueprint-list'),
    url(r'^projects/(?P<project_slug>[-\w_]+)/blueprints/'
        r'(?P<blueprint_slug>[-\w_]+)/$',
        views.ModuleCreateView.as_view(),
        name='module-create'),
    url(r'^publish/module/(?P<module_slug>[-\w_]+)/$',
        views.ModulePublishView.as_view(),
        name='module-publish'),
    url(r'^delete/module/(?P<slug>[-\w_]+)/$',
        views.ModuleDeleteView.as_view(),
        name='module-delete'),

    # Overwrite adhocracy4 core urls with meinBerlin urls
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/blueprints/'
        r'external-project/$',
        extproject_views.ExternalProjectCreateView.as_view(),
        name='external-project-create'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/blueprints/'
        r'bplan/$',
        bplan_views.BplanProjectCreateView.as_view(),
        name='bplan-project-create'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/blueprints/'
        r'container/$',
        container_views.ContainerCreateView.as_view(),
        name='container-create'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/projects/$',
        views.DashboardProjectListView.as_view(),
        name='project-list'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/projects/create$',
        views.ProjectCreateView.as_view(),
        name='project-create'),
] + a4dashboard_urlpatterns
