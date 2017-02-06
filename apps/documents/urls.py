from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^(?P<pk>\d+)/$',
        views.ParagraphDetailView.as_view(),
        name='paragraph-detail'
    ),
]
