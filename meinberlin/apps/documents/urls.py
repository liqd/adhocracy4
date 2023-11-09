from django.urls import path

from . import views

urlpatterns = [
    path(
        "chapters/<int:pk>/",
        views.ChapterDetailView.as_view(),
        name="chapter-detail",
    ),
    path(
        "paragraphs/<int:pk>/",
        views.ParagraphDetailView.as_view(),
        name="paragraph-detail",
    ),
]
