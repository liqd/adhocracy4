from django.conf.urls import url

from meinberlin.apps.dashboard2.urls import \
    urlpatterns as a4dashboard_urlpatterns

from . import views

app_name = 'a4dashboard'

# Overwrite the ProjectUpdateView with meinBerlin urls conf
urlpatterns = [
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/blueprints/'
        r'external-project/$',
        views.ExternalProjectCreateView.as_view(),
        name='external-project-create'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/blueprints/'
        r'bplan/$',
        views.BplanProjectCreateView.as_view(),
        name='bplan-project-create'),
] + a4dashboard_urlpatterns
