from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from adhocracy4.api.mixins import ContentTypeMixin
from adhocracy4.api.permissions import ViewSetRulesPermission
from adhocracy4.comments.models import Comment
from adhocracy4.comments.signals import comment_removed
from adhocracy4.rules.discovery import NormalUser

from .filters import CommentCategoryFilterBackend
from .filters import CommentOrderingFilterBackend
from .filters import CustomSearchFilter
from .serializers import ThreadListSerializer
from .serializers import ThreadSerializer


class CommentSetPagination(PageNumberPagination):
    page_size = 100


class PaginationCommentLinkMixin:
    def list(self, request, content_type=None, object_pk=None):
        """
        Add comment_found info to data when commentID is in request.

        Attention: No super, be careful with order of inheritance!
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            if "commentID" in request.query_params:
                try:
                    commentID = int(request.query_params["commentID"])
                    if queryset.filter(id=commentID).exists():
                        response.data["comment_found"] = True
                    else:
                        parent = [
                            item
                            for item in queryset.values_list("id", "child_comments")
                            if item[1] == commentID
                        ]
                        if parent:
                            response.data["comment_found"] = True
                            response.data["comment_parent"] = parent[0][0]
                        else:
                            response.data["comment_found"] = False
                except ValueError:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            return response
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PermissionInfoMixin:
    def list(self, request, *args, **kwargs):
        """Add commenting_permissions to response's data."""
        response = super().list(request, args, kwargs)
        if response.status_code == 400:
            return response

        obj = self.content_object
        contenttype = ContentType.objects.get_for_model(obj)
        permission = "{ct.app_label}.comment_{ct.model}".format(ct=contenttype)

        has_commenting_permission = False
        would_have_commenting_permission = NormalUser().would_have_perm(permission, obj)

        if hasattr(request, "user"):
            has_commenting_permission = request.user.has_perm(permission, obj)

        response.data["has_commenting_permission"] = has_commenting_permission
        response.data[
            "would_have_commenting_permission"
        ] = would_have_commenting_permission
        response.data["project_is_public"] = obj.project.is_public
        return response


class CommentViewSet(
    PermissionInfoMixin,  # needs to be first, has super(list)
    PaginationCommentLinkMixin,  # needs to be second, no super
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    ContentTypeMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (ViewSetRulesPermission,)
    filter_backends = (
        filters.DjangoFilterBackend,
        CommentOrderingFilterBackend,
        CommentCategoryFilterBackend,
        CustomSearchFilter,
    )
    filterset_fields = ("object_pk", "content_type")
    ordering = "-created"
    content_type_filter = settings.A4_COMMENTABLES
    pagination_class = CommentSetPagination
    search_fields = ("comment", "=creator__username")

    def get_serializer_class(self):
        if self.action == "list":
            return ThreadListSerializer
        return ThreadSerializer

    def _save_terms_agreement(self):
        if (
            hasattr(settings, "A4_USE_ORGANISATION_TERMS_OF_USE")
            and settings.A4_USE_ORGANISATION_TERMS_OF_USE
            and not self._user_has_agreed(self.request.user)
        ):
            if (
                "agreed_terms_of_use" in self.request.data
                and self.request.data["agreed_terms_of_use"]
            ):
                OrganisationTermsOfUse = self._get_org_terms_model()
                OrganisationTermsOfUse.objects.update_or_create(
                    user=self.request.user,
                    organisation=self.content_object.project.organisation,
                    defaults={"has_agreed": self.request.data["agreed_terms_of_use"]},
                )
            else:
                raise ValidationError(
                    {"comment": _("Please agree to the organisation's terms of use.")}
                )

    def perform_create(self, serializer):
        self._save_terms_agreement()
        serializer.save(content_object=self.content_object, creator=self.request.user)

    def perform_update(self, serializer):
        self._save_terms_agreement()
        serializer.save()

    def get_permission_object(self):
        return self.content_object

    def get_queryset(self):
        child_comment_content_type_id = ContentType.objects.get_for_model(Comment)
        comments = Comment.objects.filter(object_pk=self.object_pk).filter(
            content_type_id=self.content_type.pk
        )
        if self.action == "list":
            return comments.exclude(
                content_type_id=child_comment_content_type_id
            ).order_by("-created")
        return comments

    @property
    def rules_method_map(self):
        return ViewSetRulesPermission.default_rules_method_map._replace(
            POST="{app_label}.comment_{model}".format(
                app_label=self.content_type.app_label, model=self.content_type.model
            )
        )

    def _get_org_terms_model(self):
        """Make sure, only used with A4_USE_ORGANISATION_TERMS_OF_USE."""
        organisation_model = apps.get_model(settings.A4_ORGANISATIONS_MODEL)
        OrganisationTermsOfUse = apps.get_model(
            organisation_model._meta.app_label, "OrganisationTermsOfUse"
        )
        return OrganisationTermsOfUse

    def _user_has_agreed(self, user):
        OrganisationTermsOfUse = self._get_org_terms_model()
        organisation = self.content_object.project.organisation
        user_has_agreed = OrganisationTermsOfUse.objects.filter(
            user=user, organisation=organisation, has_agreed=True
        ).exists()
        return user_has_agreed

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if self.request.user == comment.creator:
            comment.is_removed = True
        else:
            comment.is_censored = True
        # saving a removed or censored comment sets its comment text
        # and comment_categories to '' (see models save method)
        comment.save()
        comment_removed.send(sender=type(comment), instance=comment)
        serializer = self.get_serializer(comment)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """Add organisation terms of use info to response.data."""
        response = super().list(request, args, kwargs)
        if response.status_code == 400:
            return response

        use_org_terms_of_use = False
        if (
            hasattr(settings, "A4_USE_ORGANISATION_TERMS_OF_USE")
            and settings.A4_USE_ORGANISATION_TERMS_OF_USE
        ):
            user_has_agreed = None
            use_org_terms_of_use = True
            organisation = self.content_object.project.organisation
            try:
                org_terms_url = reverse(
                    "organisation-terms-of-use",
                    kwargs={"organisation_slug": organisation.slug},
                )
            except NoReverseMatch:
                raise NotImplementedError("Add org terms of use view.")
            if hasattr(request, "user"):
                user = request.user
                if user.is_authenticated:
                    user_has_agreed = self._user_has_agreed(user)
            response.data["user_has_agreed"] = user_has_agreed
            response.data["org_terms_url"] = org_terms_url
        response.data["use_org_terms_of_use"] = use_org_terms_of_use
        return response
