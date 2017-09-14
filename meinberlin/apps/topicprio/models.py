from django.core.urlresolvers import reverse

from meinberlin.apps.ideas.models import AbstractIdea


class Topic(AbstractIdea):

    def get_absolute_url(self):
        return reverse('meinberlin_topicprio:topic-detail',
                       args=[str(self.slug)])

    class Meta:
        ordering = ['-created']
