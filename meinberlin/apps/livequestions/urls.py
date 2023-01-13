from django.urls import re_path

from . import views

urlpatterns = [
    re_path(
        r"present/module/(?P<module_slug>[-\w_]+)/$",
        views.LiveQuestionPresentationListView.as_view(),
        name="question-present",
    ),
]
