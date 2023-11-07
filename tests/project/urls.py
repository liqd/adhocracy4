from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import include
from django.urls import path
from rest_framework import routers

from adhocracy4.api import routers as a4routers
from adhocracy4.comments.api import CommentViewSet
from adhocracy4.comments_async.api import CommentViewSet as CommentViewSetAsync
from adhocracy4.dashboard import urls as dashboard_urls
from adhocracy4.follows.api import FollowViewSet
from adhocracy4.modules import urls as mod_urls
from adhocracy4.polls.api import PollViewSet
from adhocracy4.projects import urls as prj_urls
from adhocracy4.ratings.api import RatingViewSet
from adhocracy4.reports.api import ReportViewSet

router = routers.DefaultRouter()
router.register(r"follows", FollowViewSet, basename="follows")
router.register(r"reports", ReportViewSet, basename="reports")
router.register(r"polls", PollViewSet, basename="polls")

ct_router = a4routers.ContentTypeDefaultRouter()
ct_router.register(r"comments", CommentViewSet, basename="comments")
ct_router.register(r"comments_async", CommentViewSetAsync, basename="comments_async")
ct_router.register(r"ratings", RatingViewSet, basename="ratings")

urlpatterns = [
    path("api/", include(ct_router.urls)),
    path("api/", include(router.urls)),
    path("admin/", admin.site.urls),
    path("projects/", include(prj_urls)),
    path("modules/", include(mod_urls)),
    path("accounts/login", LoginView.as_view(), name="account_login"),
    path("dashboard/", include(dashboard_urls)),
]
