from rest_framework import routers

from adhocracy4.api.routers import CustomRouterMixin


class TokenVoteRouterMixin(CustomRouterMixin):

    prefix_regex = (
        r'contenttypes/(?P<content_type>[\d]+)/{prefix}'
    )


class TokenVoteDefaultRouter(TokenVoteRouterMixin, routers.DefaultRouter):
    pass
