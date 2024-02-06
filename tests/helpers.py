import re

from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site


class pytest_regex:
    """Assert that a given string meets some expectations."""

    def __init__(self, pattern, flags=0):
        self._regex = re.compile(pattern, flags)

    def __eq__(self, actual):
        return bool(self._regex.match(str(actual)))

    def __repr__(self):
        return self._regex.pattern


def clear_query_cache():
    """Clear the cache for GenericRelations.
    Required for django_assert_num_queries to work correctly, as otherwise
    some queries will be cached. Call directly before django_assert_num_queries."""
    ContentType.objects.clear_cache()
    Site.objects.clear_cache()
