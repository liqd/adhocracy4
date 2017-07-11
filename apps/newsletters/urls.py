from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^create/$',
        views.NewsletterCreateView.as_view(), name='newsletter-create'),
    url(r'^(?P<pk>\d+)/update/$',
        views.NewsletterUpdateView.as_view(), name='newsletter-update'),
]
