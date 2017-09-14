from django.core.urlresolvers import reverse

from meinberlin.apps.mapideas.models import AbstractMapIdea


class MapTopic(AbstractMapIdea):

    class Meta:
        ordering = ['-created']

    def get_absolute_url(self):
        return reverse('meinberlin_maptopicprio:maptopic-detail',
                       args=[str(self.slug)])
