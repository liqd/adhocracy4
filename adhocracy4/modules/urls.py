from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<module_slug>[-\w_]+)/$', views.ModuleDetailView.as_view(),
        name='module-detail'),
]
