# Orignal version taken from http://www.djangosnippets.org/snippets/186/
# Original author: udfalkso

import cProfile
import pstats
from io import StringIO

from django.conf import settings


class ProfileMiddleware(object):
    """
    Displays cProfile profiling for any view.

    First add this as the first middleware to your `MIDDLEWARE_CLASSES`
    settings. Add the "prof" key to query string by appending ?prof (or &prof=)
    and you'll see the profiling results in your browser.
    """
    def process_request(self, request):
        if settings.DEBUG and 'prof' in request.GET:
            prof = cProfile.Profile()
            prof.enable()
            self.prof = prof

    def process_response(self, request, response):
        if settings.DEBUG and 'prof' in request.GET:
            out = StringIO()
            prof = self.prof
            prof.disable()

            stats = pstats.Stats(prof, stream=out)
            stats.sort_stats('cumtime')
            stats.print_stats()
            stats_str = out.getvalue()

            if response and response.content and stats_str:
                response.content = "<pre>" + stats_str + "</pre>"
        return response
