from rest_framework import routers


class ContentTypeRouterMixin():

    prefix_regex = (
        'contenttypes/(?P<content_type>[\d]+)/'
        'objects/(?P<object_pk>[\d]+)/{prefix}'
    )

    @property
    def routes(self):
        routes = super().routes
        return [route._replace(url=route.url.replace('{prefix}',
                                                     self.prefix_regex))
                for route in routes]


class ContentTypeSimpleRouter(ContentTypeRouterMixin, routers.SimpleRouter):
    pass


class ContentTypeDefaultRouter(ContentTypeRouterMixin, routers.DefaultRouter):
    pass
