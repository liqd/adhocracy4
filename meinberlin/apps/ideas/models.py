from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from django.contrib.contenttypes.fields import GenericRelation
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from adhocracy4 import transforms
from adhocracy4.categories.fields import CategoryField
from adhocracy4.comments import models as comment_models
from adhocracy4.models import query
from adhocracy4.modules import models as module_models
from adhocracy4.ratings import models as rating_models


class IdeaQuerySet(query.RateableQuerySet, query.CommentableQuerySet):
    pass


class AbstractIdea(module_models.Item):
    item_ptr = models.OneToOneField(to=module_models.Item,
                                    parent_link=True,
                                    related_name='%(app_label)s_%(class)s')
    slug = AutoSlugField(populate_from='name', unique=True)
    name = models.CharField(max_length=120, verbose_name=_('Title'))
    description = RichTextField(verbose_name=_('Description'))
    ratings = GenericRelation(rating_models.Rating,
                              related_query_name='idea',
                              object_id_field='object_pk')
    comments = GenericRelation(comment_models.Comment,
                               related_query_name='idea',
                               object_id_field='object_pk')
    category = CategoryField()

    objects = IdeaQuerySet.as_manager()

    @property
    def reference_number(self):
        return '{:d}-{:05d}'.format(self.created.year, self.pk)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.description = transforms.clean_html_field(
            self.description)
        super().save(*args, **kwargs)


class Idea(AbstractIdea):

    def get_absolute_url(self):
        return reverse('meinberlin_ideas:idea-detail',
                       kwargs=dict(pk='{:05d}'.format(self.pk),
                                   year=self.created.year))

    class Meta:
        ordering = ['-created']
