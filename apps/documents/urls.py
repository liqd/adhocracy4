from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^chapters/(?P<pk>\d+)/$',
        views.ChapterDetailView.as_view(),
        name='chapter-detail'
    ),
    url(
        r'^paragraphs/(?P<pk>\d+)/$',
        views.ParagraphDetailView.as_view(),
        name='paragraph-detail'
    ),
    url(
        r'^manage/chapters/(?P<pk>\d+)/$',
        views.ChapterManagementView.as_view(),
        name='chapter-management'
    ),
]
