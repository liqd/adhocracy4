from rest_framework import serializers

from adhocracy4.projects import models as project_models

from . import models


class FollowSerializer(serializers.ModelSerializer):

    project = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    follows = serializers.SerializerMethodField()
    creator = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = models.Follow
        read_only_field = ('project', 'creator', 'created', 'modified')
        exclude = ('id',)

    def save(self, *args, **kwargs):
        if 'project__slug' in kwargs:
            slug = kwargs.pop('project__slug')
            project = project_models.Project.objects.get(slug=slug)
            kwargs['project'] = project
        return super().save(*args, **kwargs)

    def get_follows(self, obj):
        return models.Follow.objects.filter(
            project=obj.project,
            enabled=True
        ).count()
