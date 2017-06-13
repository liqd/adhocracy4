from autoslug import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from adhocracy4 import transforms
from adhocracy4.categories import models as category_models
from adhocracy4.comments import models as comment_models
from adhocracy4.models import query
from adhocracy4.modules import models as module_models
from adhocracy4.ratings import models as rating_models


class TopicQuerySet(query.RateableQuerySet, query.CommentableQuerySet):
    pass


class Topic(module_models.Item, category_models.Categorizable):
    slug = AutoSlugField(populate_from='name', unique=True)
    name = models.CharField(max_length=120)
    description = RichTextUploadingField(config_name='image-editor')
    ratings = GenericRelation(rating_models.Rating,
                              related_query_name='topic',
                              object_id_field='object_pk')
    comments = GenericRelation(comment_models.Comment,
                               related_query_name='topic',
                               object_id_field='object_pk')

    objects = TopicQuerySet.as_manager()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.description = transforms.clean_html_field(
            self.description, 'image-editor')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('meinberlin_topicprio:topic-detail',
                       args=[str(self.slug)])
