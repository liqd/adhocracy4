from urllib.parse import quote

from django.utils.deprecation import MiddlewareMixin


class AjaxPathMiddleware(MiddlewareMixin):
    """Append request path as a header.

    In an ajax request, redirects are handled implicitly, so it it not possible
    to know the path of the page where you end up. This middleware adds that
    information in a header.
    """

    def process_response(self, request, response):
        response["x-ajax-path"] = quote(request.path)
        return response
