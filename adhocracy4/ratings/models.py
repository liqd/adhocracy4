from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from adhocracy4.models.base import UserGeneratedContentModel


class Rating(UserGeneratedContentModel):

    POSITIVE = 1
    NEGATIVE = -1

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    object_pk = models.PositiveIntegerField()
    content_object = GenericForeignKey(
        ct_field="content_type", fk_field="object_pk")
    value = models.IntegerField()

    class Meta:
        unique_together = ('content_type', 'object_pk', 'creator')
        index_together = [('content_type', 'object_pk')]

    def __str__(self):
        return str(self.value)

    @property
    def module(self):
        co = self.content_object
        return co.module

    @property
    def project(self):
        co = self.content_object
        return co.project

    def save(self, *args, **kwargs):
        self.value = self._get_value(self.value)
        return super().save(*args, **kwargs)

    def _get_value(self, number):
        if number > self.POSITIVE:
            return self.POSITIVE
        elif number < self.NEGATIVE:
            return self.NEGATIVE
        else:
            return number

    def get_meta_info(self, user):

        ratings = Rating.objects.filter(
            content_type=self.content_type, object_pk=self.object_pk)
        positive_ratings_on_same_object = ratings.filter(
            value=self.POSITIVE).count()
        negative_ratings_on_same_object = ratings.filter(
            value=self.NEGATIVE).count()

        try:
            user_rating_on_same_object = ratings.get(creator=user)
            user_rating_on_same_object_val = user_rating_on_same_object.value
            user_rating_on_same_object_id = user_rating_on_same_object.pk
        except ObjectDoesNotExist:
            user_rating_on_same_object_val = None
            user_rating_on_same_object_id = None

        result = {
            'positive_ratings_on_same_object': positive_ratings_on_same_object,
            'negative_ratings_on_same_object': negative_ratings_on_same_object,
            'user_rating_on_same_object_value': user_rating_on_same_object_val,
            'user_rating_on_same_object_id': user_rating_on_same_object_id
        }

        return result

    def update(self, value):
        self.value = 0
        self.save()
