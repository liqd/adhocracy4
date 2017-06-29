from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^project/(?P<project_slug>[-\w_]+)/$',
        views.ExportProjectDispatcher.as_view(), name='export-project'),
    url(r'^module/(?P<module_slug>[-\w_]+)/(?P<export_id>\d+)/$',
        views.ExportModuleDispatcher.as_view(), name='export-module'),
]
