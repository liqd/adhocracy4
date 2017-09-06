from django.conf.urls import url

from meinberlin.apps.dashboard2.urls import \
    urlpatterns as a4dashboard_urlpatterns

from . import views

app_name = 'a4dashboard'

urlpatterns = [
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/settings/$',
        views.DashboardOrganisationUpdateView.as_view(),
        name='organisation-edit'),
    url(r'^newsletters/(?P<organisation_slug>[-\w_]+)/create/$',
        views.DashboardNewsletterCreateView.as_view(),
        name='newsletter-create'),

    # Overwrite the ProjectUpdateView with meinBerlin urls
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/blueprints/'
        r'external-project/$',
        views.ExternalProjectCreateView.as_view(),
        name='external-project-create'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/blueprints/'
        r'bplan/$',
        views.BplanProjectCreateView.as_view(),
        name='bplan-project-create'),
] + a4dashboard_urlpatterns
