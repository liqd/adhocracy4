from django.urls import re_path

from . import views

urlpatterns = [
    re_path(
        r'^chapters/(?P<pk>\d+)/$',
        views.ChapterDetailView.as_view(),
        name='chapter-detail'
    ),
    re_path(
        r'^paragraphs/(?P<pk>\d+)/$',
        views.ParagraphDetailView.as_view(),
        name='paragraph-detail'
    ),
]
