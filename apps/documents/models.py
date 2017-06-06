from ckeditor.fields import RichTextField
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.functional import cached_property

from adhocracy4 import transforms
from adhocracy4.comments import models as comment_models
from adhocracy4.models import base
from adhocracy4.modules import models as module_models


class Chapter(module_models.Item):
    name = models.CharField(max_length=120)
    comments = GenericRelation(comment_models.Comment,
                               related_query_name='chapter',
                               object_id_field='object_pk')
    # weight = models.PositiveIntegerField()

    def __str__(self):
        return "{}_chapter_{}".format(str(self.module), self.pk)

    # FIXME: adapt absolute url!
    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('project-detail', args=[str(self.project.slug)])


class Paragraph(base.TimeStampedModel):
    name = models.CharField(max_length=120, blank=True)
    text = RichTextField()
    weight = models.PositiveIntegerField()
    chapter = models.ForeignKey(Chapter,
                                on_delete=models.CASCADE,
                                related_name='paragraphs')
    comments = GenericRelation(comment_models.Comment,
                               related_query_name='paragraph',
                               object_id_field='object_pk')

    class Meta:
        ordering = ('weight',)

    def __str__(self):
        return "{}_paragraph_{}".format(str(self.chapter), self.weight)

    def save(self, *args, **kwargs):
        self.text = transforms.clean_html_field(
            self.text, 'image-editor')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('meinberlin_documents:paragraph-detail',
                       args=[str(self.pk)])

    @cached_property
    def creator(self):
        return self.chapter.creator

    @cached_property
    def project(self):
        return self.chapter.project
