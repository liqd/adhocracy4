from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<slug>[-\w_]+)/$',
        views.ProposalDetailView.as_view(), name='proposal-detail'),
    url(r'create/module/(?P<slug>[-\w_]+)/$',
        views.ProposalCreateView.as_view(), name='proposal-create'),
    url(r'^(?P<slug>[-\w_]+)/update/$',
        views.ProposalUpdateView.as_view(), name='proposal-update'),
    url(r'^(?P<slug>[-\w_]+)/delete/$',
        views.ProposalDeleteView.as_view(), name='proposal-delete'),
    url(r'^(?P<slug>[-\w_]+)/moderate/$',
        views.ProposalModerateView.as_view(), name='proposal-moderate'),
]
