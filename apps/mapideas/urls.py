from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<slug>[-\w_]+)/$',
        views.MapIdeaDetailView.as_view(), name='idea-detail'),
    url(r'create/module/(?P<slug>[-\w_]+)/$',
        views.MapIdeaCreateView.as_view(), name='idea-create'),
    url(r'^(?P<slug>[-\w_]+)/update/$',
        views.MapIdeaUpdateView.as_view(), name='idea-update'),
    url(r'^(?P<slug>[-\w_]+)/delete/$',
        views.MapIdeaDeleteView.as_view(), name='idea-delete'),
]
