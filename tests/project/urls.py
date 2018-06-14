from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views
from rest_framework import routers

from adhocracy4.api import routers as a4routers
from adhocracy4.dashboard import urls as dashboard_urls
from adhocracy4.modules import urls as mod_urls
from adhocracy4.projects import urls as prj_urls
from adhocracy4.follows.api import FollowViewSet
from adhocracy4.ratings.api import RatingViewSet
from adhocracy4.reports.api import ReportViewSet
from adhocracy4.polls.api import PollViewSet, VoteViewSet
from adhocracy4.comments.api import CommentViewSet
from adhocracy4.polls.routers import QuestionDefaultRouter

router = routers.DefaultRouter()
router.register(r'follows', FollowViewSet, base_name='follows')
router.register(r'reports', ReportViewSet, base_name='reports')
router.register(r'polls', PollViewSet, base_name='polls')

question_router = QuestionDefaultRouter()
question_router.register(r'vote', VoteViewSet, base_name='votes')

ct_router = a4routers.ContentTypeDefaultRouter()
ct_router.register(r'comments', CommentViewSet, base_name='comments')
ct_router.register(r'ratings', RatingViewSet, base_name='ratings')

urlpatterns = [
    url(r'^api/', include(ct_router.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^api/', include(question_router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^projects/', include(prj_urls)),
    url(r'^modules/', include(mod_urls)),
    url(r'^accounts/login', views.login, name='account_login'),
    url(r'^dashboard/', include(dashboard_urls))
]
