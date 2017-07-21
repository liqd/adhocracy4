from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<slug>[-\w_]+)/$',
        views.IdeaDetailView.as_view(), name='idea-detail'),
    url(r'create/module/(?P<slug>[-\w_]+)/$',
        views.IdeaCreateView.as_view(), name='idea-create'),
    url(r'^(?P<slug>[-\w_]+)/update/$',
        views.IdeaUpdateView.as_view(), name='idea-update'),
    url(r'^(?P<slug>[-\w_]+)/delete/$',
        views.IdeaDeleteView.as_view(), name='idea-delete'),
]
