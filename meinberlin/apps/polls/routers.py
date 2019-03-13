from rest_framework import routers

from adhocracy4.api.routers import CustomRouterMixin


class QuestionRouterMixin(CustomRouterMixin):

    prefix_regex = (
        r'polls/question/(?P<question_pk>[\d]+)/{prefix}'
    )


class QuestionSimpleRouter(QuestionRouterMixin, routers.SimpleRouter):
    pass


class QuestionDefaultRouter(QuestionRouterMixin, routers.DefaultRouter):
    pass
