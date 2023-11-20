from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from adhocracy4 import transforms
from adhocracy4.categories.fields import CategoryField
from adhocracy4.models.base import TimeStampedModel
from adhocracy4.modules import models as module_models


class AnonymousItem(TimeStampedModel):
    module = models.ForeignKey(module_models.Module, on_delete=models.CASCADE)

    @property
    def project(self):
        return self.module.project

    @property
    def creator(self):
        return AnonymousUser()

    @creator.setter
    def creator(self, value):
        pass

    class Meta:
        abstract = True


class LikeQuerySet(models.QuerySet):
    def annotate_like_count(self):
        return self.annotate(like_count=models.Count("question_likes", distinct=True))


class LiveQuestion(AnonymousItem):
    text = models.TextField(max_length=1000, verbose_name=_("Question"))
    is_answered = models.BooleanField(default=False)
    is_on_shortlist = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    is_live = models.BooleanField(default=False)

    category = CategoryField(verbose_name=_("Characteristic"))

    objects = LikeQuerySet.as_manager()

    def __str__(self):
        return str(self.text)

    def get_absolute_url(self):
        return reverse("module-detail", args=[str(self.module.slug)])


class LiveStream(module_models.Item):
    live_stream = CKEditor5Field(
        verbose_name="Livestream",
        blank=True,
        config_name="video-editor",
        help_text=_(
            "You can enter a livestream from YouTube or Vimeo. "
            "The livestream will be shown when the module phase "
            "is active. For description text please use module "
            "or phase description."
        ),
    )

    def save(self, update_fields=None, *args, **kwargs):
        if self.live_stream and "<iframe" in self.live_stream:
            self.live_stream = transforms.clean_html_field(
                self.live_stream, "video-editor"
            )
            if update_fields:
                update_fields = {"live_stream"}.union(update_fields)
            super().save(update_fields=update_fields, *args, **kwargs)
        elif self.__class__.objects.filter(module=self.module).exists():
            for stream in self.__class__.objects.filter(module=self.module):
                stream.delete()
