from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

from adhocracy4.api.mixins import ModuleMixin
from adhocracy4.api.permissions import ViewSetRulesPermission
from adhocracy4.categories import get_category_icon_url
from adhocracy4.categories import has_icons
from adhocracy4.categories.models import Category
from adhocracy4.labels.models import Label
from adhocracy4.modules.predicates import is_allowed_moderate_project
from adhocracy4.modules.predicates import module_is_between_phases
from adhocracy4.phases.predicates import has_feature_active
from meinberlin.apps.contrib.filters import OrderingFilterWithDailyRandom
from meinberlin.apps.contrib.templatetags.contrib_tags import (
    get_proper_elided_page_range,
)
from meinberlin.apps.moderationtasks.models import ModerationTask
from meinberlin.apps.moderatorfeedback.models import (
    DEFAULT_CHOICES as moderator_status_default_choices,
)
from meinberlin.apps.votes.api import VotingTokenInfoMixin
from meinberlin.apps.votes.filters import OwnVotesFilterBackend

from .filters import ProposalFilterBackend
from .filters import ProposalFilterSet
from .models import Proposal
from .serializers import ProposalSerializer


# To be changed to a more general IdeaPagination, when using
# pagination via rest api for more idea lists
class ProposalPagination(PageNumberPagination):
    page_size = 15

    def get_paginated_response(self, data):
        response = super(ProposalPagination, self).get_paginated_response(data)
        response.data["page_size"] = self.page_size
        response.data["page_count"] = self.page.paginator.num_pages
        response.data["page_elided_range"] = get_proper_elided_page_range(
            self.page.paginator, self.page.number
        )
        return response


class LocaleInfoMixin:
    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        response.data["locale"] = get_language()
        return response


class ProposalFilterInfoMixin:
    def list(self, request, *args, **kwargs):
        """Add the filter information to the data of the Proposal API.

        Needs to be used with rest_framework.mixins.ListModelMixin
        and adhocracy4.api.mixins.ModuleMixin or some other mixin that
        fetches the module
        """
        filters = {}

        # category filter
        category_choices, category_icons = self.get_category_choices_and_icons()
        if category_choices:
            filters["category"] = {
                "label": _("Category"),
                "choices": category_choices,
            }
            if category_icons:
                filters["category"]["icons"] = category_icons

        # label filter
        label_choices = self.get_label_choices()
        if label_choices:
            filters["labels"] = {
                "label": _("Label"),
                "choices": label_choices,
            }

        # archived filter
        filters["is_archived"] = {
            "label": _("Archived"),
            "choices": [
                ("", _("All")),
                ("false", _("No")),
                ("true", _("Yes")),
            ],
            "default": "false",
        }

        # moderator feedback filter
        moderator_status_choices = [("", _("All"))] + [
            choice for choice in moderator_status_default_choices
        ]

        filters["moderator_status"] = {
            "label": _("Status"),
            "choices": moderator_status_choices,
        }

        # own votes filter
        # only show during voting phase and when token is entered
        if (
            has_feature_active(self.module, Proposal, "vote")
            and "voting_tokens" in request.session
            and str(self.module.id) in request.session["voting_tokens"]
        ):
            filters["own_votes"] = {
                "label": _("Voting"),
                "choices": [
                    ("", _("All")),
                    ("true", _("My votes")),
                ],
            }

        # moderation task filter, only show to moderators
        if is_allowed_moderate_project(request.user, self.module):
            moderation_task_choices = self.get_moderation_task_choices()
            if moderation_task_choices:
                filters["open_task"] = {
                    "label": _("Open tasks"),
                    "choices": moderation_task_choices,
                }

        # ordering filter
        ordering_choices = self.get_ordering_choices(request)
        default_ordering = self.get_default_ordering()
        filters["ordering"] = {
            "label": _("Ordering"),
            "choices": ordering_choices,
            "default": default_ordering,
        }

        response = super().list(request, args, kwargs)
        response.data["filters"] = filters
        return response

    def get_category_choices_and_icons(self):
        category_choices = category_icons = None
        categories = Category.objects.filter(module=self.module)
        if categories:
            category_choices = [
                ("", _("All")),
            ]
            if has_icons(self.module):
                category_icons = []
            for category in categories:
                category_choices += ((str(category.pk), category.name),)
                if has_icons(self.module):
                    icon_name = getattr(category, "icon", None)
                    icon_url = get_category_icon_url(icon_name)
                    category_icons += ((str(category.pk), icon_url),)
        return category_choices, category_icons

    def get_label_choices(self):
        label_choices = None
        labels = Label.objects.filter(module=self.module)
        if labels:
            label_choices = [
                ("", _("All")),
            ]
            for label in labels:
                label_choices += ((str(label.pk), label.name),)

        return label_choices

    def get_moderation_task_choices(self):
        moderation_task_choices = None
        moderation_tasks = ModerationTask.objects.filter(module=self.module)
        if moderation_tasks:
            moderation_task_choices = [
                ("", _("All")),
            ]
            for task in moderation_tasks:
                moderation_task_choices += ((str(task.pk), task.name),)

        return moderation_task_choices

    def get_ordering_choices(self, request):
        ordering_choices = [
            ("-created", _("Most recent")),
        ]
        # only show sort by rating when rating is allowed at anytime in module
        # like "view_rate_count" from PermissionInfoMixin
        if self.module.has_feature("rate", Proposal):
            ordering_choices += (("-positive_rating_count", _("Most popular")),)
        # only show sort by support option during support phase and btw support
        # and voting phase like "view_support_count" from PermissionInfoMixin
        show_support_option = request.user.has_perm(
            "meinberlin_budgeting.view_support", self.module
        )
        if show_support_option:
            ordering_choices += (("-positive_rating_count", _("Most support")),)
        ordering_choices += (
            ("-comment_count", _("Most commented")),
            ("dailyrandom", _("Random")),
        )

        return ordering_choices

    def get_default_ordering(self):
        """Return current default of ordering filter.

        Between support and voting phase, 'most support' is default ordering
        filter, else dailyrandom
        """
        if module_is_between_phases(
            "meinberlin_budgeting:support", "meinberlin_budgeting:voting", self.module
        ):
            return "-positive_rating_count"
        return "dailyrandom"


class PermissionInfoMixin:
    def list(self, request, *args, **kwargs):
        """Add the permission information to the data of the Proposal API.

        Needs to be used with rest_framework.mixins.ListModelMixin
        and adhocracy4.api.mixins.ModuleMixin or some other mixin that
        fetches the module
        """
        permissions = {}
        user = request.user
        permissions["view_support_count"] = user.has_perm(
            "meinberlin_budgeting.view_support", self.module
        )
        permissions["view_rate_count"] = self.module.has_feature("rate", Proposal)
        permissions["view_comment_count"] = self.module.has_feature("comment", Proposal)
        permissions["view_vote_count"] = has_feature_active(
            self.module, Proposal, "vote"
        )

        response = super().list(request, args, kwargs)
        response.data["permissions"] = permissions
        return response


class ProposalViewSet(
    ModuleMixin,
    ProposalFilterInfoMixin,
    PermissionInfoMixin,
    LocaleInfoMixin,
    VotingTokenInfoMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):

    pagination_class = ProposalPagination
    serializer_class = ProposalSerializer
    permission_classes = (ViewSetRulesPermission,)
    filter_backends = (
        ProposalFilterBackend,
        OrderingFilterWithDailyRandom,
        SearchFilter,
        OwnVotesFilterBackend,
    )

    # this is used by ProposalFilterBackend
    filterset_class = ProposalFilterSet

    ordering_fields = (
        "created",
        "comment_count",
        "positive_rating_count",
        "dailyrandom",
    )
    search_fields = ("name", "ref_number")

    @property
    def ordering(self):
        if module_is_between_phases(
            "meinberlin_budgeting:support", "meinberlin_budgeting:voting", self.module
        ):
            return ["-positive_rating_count"]
        return ["dailyrandom"]

    def get_permission_object(self):
        return self.module

    def get_queryset(self):
        proposals = (
            Proposal.objects.filter(module=self.module)
            .annotate_comment_count()
            .annotate_positive_rating_count()
            .annotate_reference_number()
            .order_by("-created")
        )
        return proposals
