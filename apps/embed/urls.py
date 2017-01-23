from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',
        views.EmbedView.as_view(), name='idea-embed'),
]
