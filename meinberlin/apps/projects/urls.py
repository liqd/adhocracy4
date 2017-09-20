from django.conf.urls import url

from adhocracy4.projects.urls import urlpatterns as a4_projects_urls

from . import views

urlpatterns = [
    url(r'^$', views.ProjectListView.as_view(),
        name='project-list'),
    url(r'^participant-invites/(?P<invite_token>[-\w_]+)/$',
        views.ParticipantInviteDetailView.as_view(),
        name='project-participant-invite-detail'),
    url(r'^participant-invites/(?P<invite_token>[-\w_]+)/accept/$',
        views.ParticipantInviteUpdateView.as_view(),
        name='project-participant-invite-update'),
    url(r'^moderator-invites/(?P<invite_token>[-\w_]+)/$',
        views.ModeratorInviteDetailView.as_view(),
        name='project-moderator-invite-detail'),
    url(r'^moderator-invites/(?P<invite_token>[-\w_]+)/accept/$',
        views.ModeratorInviteUpdateView.as_view(),
        name='project-moderator-invite-update'),
]

urlpatterns += a4_projects_urls
