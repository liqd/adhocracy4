from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views

from adhocracy4.projects import urls as prj_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^projects/', include(prj_urls)),
    url(r'^accounts/login', views.login, name="account_login")
]
