from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<year>\d{4})-(?P<pk>\d+)/$',
        views.IdeaDetailView.as_view(), name='idea-detail'),
    url(r'^(?P<slug>[-\w_]+)/$',
        views.IdeaDetailView.as_view(), name='idea-redirect'),
    url(r'create/module/(?P<module_slug>[-\w_]+)/$',
        views.IdeaCreateView.as_view(), name='idea-create'),
    url(r'^(?P<year>\d{4})-(?P<pk>\d+)/update/$',
        views.IdeaUpdateView.as_view(), name='idea-update'),
    url(r'^(?P<year>\d{4})-(?P<pk>\d+)/delete/$',
        views.IdeaDeleteView.as_view(), name='idea-delete'),
    url(r'^(?P<year>\d{4})-(?P<pk>\d+)/moderate/$',
        views.IdeaModerateView.as_view(), name='idea-moderate'),
]
