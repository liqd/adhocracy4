from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/settings/$',
        views.DashboardOrganisationUpdateView.as_view(),
        name='dashboard-organisation-edit'),
    url(r'^newsletters/(?P<organisation_slug>[-\w_]+)/create/$',
        views.DashboardNewsletterCreateView.as_view(),
        name='dashboard-newsletter-create')
]
