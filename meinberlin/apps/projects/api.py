from django.utils import timezone
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response

from adhocracy4.projects.models import Project
from meinberlin.apps.projects import serializers as project_serializers


class ProjectListViewSet(mixins.ListModelMixin,
                         viewsets.ViewSet):
    serializer_class = project_serializers.ProjectSerializer

    def allowed_projects(self):
        private_projects = Project.objects.filter(is_public=False)
        if private_projects:
            not_allowed_projects = \
                [project.id for project in private_projects if
                 not self.request.user.has_perm(
                     'a4projects.view_project', project)]
            return private_projects.exclude(id__in=not_allowed_projects)

    def list(self, request, content_type=None, object_pk=None):
        projects = Project.objects \
            .filter(is_draft=False, is_archived=False) \
            .exclude(project_type__contains=('﻿meinberlin_projectcontainers.'
                                             'ProjectContainer')) \
            .exclude(project_type__contains=('meinberlin_extprojects.'
                                             'ExternalProject')) \
            .order_by('created') \
            .select_related('administrative_district',
                            'organisation') \
            .prefetch_related('moderators',
                              'plans',
                              'organisation__initiators',
                              'module_set__phase_set')
        now = timezone.now()

        active_projects = projects \
            .filter(
                module__phase__start_date__lte=now,
                module__phase__end_date__gt=now) \
            .distinct()

        future_projects = projects.filter(
                module__phase__start_date__gt=now
        ).distinct().exclude(
            id__in=active_projects.values('id'))

        past_projects = projects.filter(
            module__phase__end_date__lt=now
        ).distinct()\
            .exclude(
                id__in=active_projects.values('id'))\
            .exclude(id__in=future_projects.values('id'))

        active_projects_projects_serializer = \
            project_serializers.ActiveProjectSerializer(
                active_projects, many=True, now=now).data

        future_projects_serializer = \
            project_serializers.FutureProjectSerializer(
                future_projects, many=True, now=now).data

        past_project_serializer = \
            project_serializers.PastProjectSerializer(
                past_projects, many=True, now=now).data

        allowed_projects = project_serializers.ProjectSerializer(
                    self.allowed_projects(),
                    many=True, now=now).data

        return Response(active_projects_projects_serializer +
                        future_projects_serializer +
                        past_project_serializer +
                        allowed_projects)
