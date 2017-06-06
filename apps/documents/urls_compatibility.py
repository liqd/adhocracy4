"""Definition of backward compatible URLs."""

from django.conf.urls import url
from django.views.generic.base import RedirectView


urlpatterns = [
    url(
        r'^(?P<pk>\d+)/$',
        RedirectView.as_view(
            pattern_name='meinberlin_documents:paragraph-detail',
            permanent=True,
        )
    ),
]
