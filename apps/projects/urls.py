from adhocracy4.projects.urls import urlpatterns as a4_projects_urls
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.ProjectListView.as_view(),
        name='project-list'),
]

urlpatterns += a4_projects_urls
