from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views
from rest_framework import routers

from adhocracy4.projects import urls as prj_urls
from adhocracy4.ratings.api import RatingViewSet
from adhocracy4.reports.api import ReportViewSet
from adhocracy4.comments.api import CommentViewSet

router = routers.DefaultRouter()
router.register(r'ratings', RatingViewSet, base_name='ratings')
router.register(r'reports', ReportViewSet, base_name='reports')
router.register(r'comments', CommentViewSet, base_name='comments')


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^projects/', include(prj_urls)),
    url(r'^accounts/login', views.login, name="account_login")
]
