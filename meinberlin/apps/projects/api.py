from django.core.cache import cache
from django.db.models import Q
from django.db.models import QuerySet
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.response import Response

from adhocracy4.projects.enums import Access
from adhocracy4.projects.models import Project
from meinberlin.apps.projects import serializers as project_serializers
from meinberlin.apps.projects.filters import StatusFilter


def get_public_projects() -> QuerySet[Project]:
    """
    Helper function to query the db and retrieve all
    public projects and their related moderators, plans,
    organisations and phases.
    """
    projects = (
        Project.objects.filter(
            Q(project_type="a4projects.Project")
            | Q(project_type="meinberlin_bplan.Bplan")
        )
        .filter(
            Q(access=Access.PUBLIC) | Q(access=Access.SEMIPUBLIC),
            is_draft=False,
            is_archived=False,
        )
        .order_by("created")
        .select_related("administrative_district", "organisation")
        .prefetch_related(
            "moderators",
            "plans",
            "organisation__initiators",
            "module_set__phase_set",
            "topics",
        )
    )
    return projects


class ProjectListViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = (DjangoFilterBackend, StatusFilter)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        now = timezone.now()
        self.now = now

    def get_queryset(self):
        projects = get_public_projects()
        return projects

    def list(self, request, *args, **kwargs):
        statustype = ""
        if "status" in self.request.GET:
            statustype = self.request.GET["status"]
        data = cache.get("projects_" + statustype)
        if data is None:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            cache.set("projects_" + statustype, data)
        return Response(data)

    def get_serializer(self, *args, **kwargs):
        if "status" in self.request.GET:
            statustype = self.request.GET["status"]
            if statustype == "activeParticipation":
                return project_serializers.ActiveProjectSerializer(
                    now=self.now, *args, **kwargs
                )
            if statustype == "futureParticipation":
                return project_serializers.FutureProjectSerializer(
                    now=self.now, *args, **kwargs
                )
            if statustype == "pastParticipation":
                return project_serializers.PastProjectSerializer(
                    now=self.now, *args, **kwargs
                )
        return project_serializers.ProjectSerializer(now=self.now, *args, **kwargs)


class PrivateProjectListViewSet(viewsets.ReadOnlyModelViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        now = timezone.now()
        self.now = now

    def get_queryset(self):
        private_projects = cache.get("private_projects")
        if private_projects is None:
            private_projects = Project.objects.filter(
                is_draft=False, is_archived=False, access=Access.PRIVATE
            )
            cache.set("private_projects", private_projects)
        if private_projects:
            not_allowed_projects = [
                project.id
                for project in private_projects
                if not self.request.user.has_perm("a4projects.view_project", project)
            ]
            return private_projects.exclude(id__in=not_allowed_projects)
        else:
            return private_projects

    def get_serializer(self, *args, **kwargs):
        return project_serializers.ProjectSerializer(now=self.now, *args, **kwargs)
