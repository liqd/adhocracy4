from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^(?P<year>\d{4})-(?P<pk>\d+)/$',
            views.ProposalDetailView.as_view(), name='proposal-detail'),
    re_path(r'^(?P<slug>[-\w_]+)/$',
            views.ProposalDetailView.as_view(), name='proposal-redirect'),
    re_path(r'create/module/(?P<module_slug>[-\w_]+)/$',
            views.ProposalCreateView.as_view(), name='proposal-create'),
    re_path(r'^(?P<year>\d{4})-(?P<pk>\d+)/update/$',
            views.ProposalUpdateView.as_view(), name='proposal-update'),
    re_path(r'^(?P<year>\d{4})-(?P<pk>\d+)/delete/$',
            views.ProposalDeleteView.as_view(), name='proposal-delete'),
    re_path(r'^(?P<year>\d{4})-(?P<pk>\d+)/moderate/$',
            views.ProposalModerateView.as_view(), name='proposal-moderate'),
]
