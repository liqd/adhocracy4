from autoslug import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from adhocracy4 import transforms
from adhocracy4.categories.fields import CategoryField
from adhocracy4.comments import models as comment_models
from adhocracy4.maps import fields as map_fields
from adhocracy4.models import query
from adhocracy4.modules import models as module_models
from adhocracy4.ratings import models as rating_models


class MapTopicQuerySet(query.RateableQuerySet, query.CommentableQuerySet):
    pass


class MapTopic(module_models.Item):
    item_ptr = models.OneToOneField(to=module_models.Item,
                                    parent_link=True,
                                    related_name='%(app_label)s_%(class)s')
    slug = AutoSlugField(populate_from='name', unique=True)
    name = models.CharField(max_length=120, verbose_name=_('Title'))
    description = RichTextUploadingField(config_name='image-editor')
    ratings = GenericRelation(rating_models.Rating,
                              related_query_name='idea',
                              object_id_field='object_pk')
    comments = GenericRelation(comment_models.Comment,
                               related_query_name='idea',
                               object_id_field='object_pk')
    category = CategoryField()
    point = map_fields.PointField(
        verbose_name=_('Where can your idea be located on a map?'),
        help_text=_('Click inside marked area on the map to set a marker. '
                    'Drag and drop the marker to change its place. '
                    'Alternatively you can use the search field to search '
                    'for an address.'))

    point_label = models.CharField(
        blank=True,
        default='',
        max_length=255,
        verbose_name=_('Label of the ideas location'),
        help_text=_('This could be an address or the name of a landmark.'),
    )

    objects = MapTopicQuerySet.as_manager()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.description = transforms.clean_html_field(
            self.description, 'image-editor')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('meinberlin_maptopicprio:maptopic-detail',
                       args=[str(self.slug)])
