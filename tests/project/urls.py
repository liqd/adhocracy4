from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views
from rest_framework import routers

from adhocracy4.api import routers as a4routers
from adhocracy4.comments.api import CommentViewSet
from adhocracy4.comments_async.api import CommentViewSet as CommentViewSetAsync
from adhocracy4.dashboard import urls as dashboard_urls
from adhocracy4.follows.api import FollowViewSet
from adhocracy4.modules import urls as mod_urls
from adhocracy4.polls.api import PollViewSet
from adhocracy4.polls.api import VoteViewSet
from adhocracy4.polls.routers import QuestionDefaultRouter
from adhocracy4.projects import urls as prj_urls
from adhocracy4.ratings.api import RatingViewSet
from adhocracy4.reports.api import ReportViewSet

router = routers.DefaultRouter()
router.register(r'follows', FollowViewSet, basename='follows')
router.register(r'reports', ReportViewSet, basename='reports')
router.register(r'polls', PollViewSet, basename='polls')

question_router = QuestionDefaultRouter()
question_router.register(r'vote', VoteViewSet, basename='votes')

ct_router = a4routers.ContentTypeDefaultRouter()
ct_router.register(r'comments', CommentViewSet, basename='comments')
ct_router.register(r'comments_async', CommentViewSetAsync,
                   basename='comments_async')
ct_router.register(r'ratings', RatingViewSet, basename='ratings')

urlpatterns = [
    url(r'^api/', include(ct_router.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^api/', include(question_router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^projects/', include(prj_urls)),
    url(r'^modules/', include(mod_urls)),
    url(r'^accounts/login', views.LoginView, name='account_login'),
    url(r'^dashboard/', include(dashboard_urls))
]
