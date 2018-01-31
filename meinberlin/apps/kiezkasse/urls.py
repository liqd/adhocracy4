from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<year>\d{4})-(?P<pk>\d+)/$',
        views.ProposalDetailView.as_view(), name='proposal-detail'),
    url(r'^(?P<slug>[-\w_]+)/$',
        views.ProposalDetailView.as_view(), name='proposal-redirect'),
    url(r'create/module/(?P<module_slug>[-\w_]+)/$',
        views.ProposalCreateView.as_view(), name='proposal-create'),
    url(r'^(?P<year>\d{4})-(?P<pk>\d+)/update/$',
        views.ProposalUpdateView.as_view(), name='proposal-update'),
    url(r'^(?P<year>\d{4})-(?P<pk>\d+)/delete/$',
        views.ProposalDeleteView.as_view(), name='proposal-delete'),
    url(r'^(?P<year>\d{4})-(?P<pk>\d+)/moderate/$',
        views.ProposalModerateView.as_view(), name='proposal-moderate'),
]
