from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^participant-invites/(?P<invite_token>[-\w_]+)/$',
            views.ParticipantInviteDetailView.as_view(),
            name='project-participant-invite-detail'),
    re_path(r'^participant-invites/(?P<invite_token>[-\w_]+)/accept/$',
            views.ParticipantInviteUpdateView.as_view(),
            name='project-participant-invite-update'),
    re_path(r'^moderator-invites/(?P<invite_token>[-\w_]+)/$',
            views.ModeratorInviteDetailView.as_view(),
            name='project-moderator-invite-detail'),
    re_path(r'^moderator-invites/(?P<invite_token>[-\w_]+)/accept/$',
            views.ModeratorInviteUpdateView.as_view(),
            name='project-moderator-invite-update'),
    re_path(r'^(?P<slug>[-\w_]+)/$', views.ProjectDetailView.as_view(),
            name='project-detail'),
    re_path(r'^module/(?P<module_slug>[-\w_]+)/$',
            views.ModuleDetailview.as_view(),
            name='module-detail')
]
