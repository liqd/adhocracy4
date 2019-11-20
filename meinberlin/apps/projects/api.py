from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from adhocracy4.projects.models import Project
from meinberlin.apps.projects import serializers as project_serializers
from meinberlin.apps.projects.filters import StatusFilter


class ProjectListViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = (DjangoFilterBackend, StatusFilter)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        now = timezone.now()
        self.now = now

    def allowed_projects(self):
        private_projects = Project.objects.filter(is_public=False)
        if private_projects:
            not_allowed_projects = \
                [project.id for project in private_projects if
                 not self.request.user.has_perm(
                     'a4projects.view_project', project)]
            return private_projects.exclude(id__in=not_allowed_projects)

    def get_queryset(self):
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
        return projects

    def get_serializer(self, *args, **kwargs):
        if 'status' in self.request.GET:
            statustype = self.request.GET["status"]
            if statustype == 'activeParticipation':
                return project_serializers.ActiveProjectSerializer(
                    now=self.now, *args, **kwargs)
            if statustype == 'futureParticipation':
                return project_serializers.FutureProjectSerializer(
                    now=self.now, *args, **kwargs)
            if statustype == 'pastParticipation':
                return project_serializers.PastProjectSerializer(
                    now=self.now, *args, **kwargs)
        return project_serializers.ProjectSerializer(
            now=self.now, *args, **kwargs)
