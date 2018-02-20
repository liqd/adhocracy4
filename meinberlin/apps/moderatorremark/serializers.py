from rest_framework import serializers

from meinberlin.apps.ideas import models as idea_models

from .models import ModeratorRemark


class ModeratorRemarkSerializer(serializers.ModelSerializer):

    idea = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    creator = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = ModeratorRemark
        read_only_fields = ('creator', 'created', 'modified')
        exclude = ('id', )

    def save(self, *args, **kwargs):
        if 'idea__slug' in kwargs:
            slug = kwargs.pop('idea__slug')
            idea = idea_models.Idea.objects.get(slug=slug)
            kwargs['idea'] = idea

        return super().save(*args, **kwargs)
