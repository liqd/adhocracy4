from django_filters import rest_framework as rest_filters

from adhocracy4.categories.models import Category
from adhocracy4.labels.models import Label
from meinberlin.apps.contrib.filters import DefaultsRestFilterSet
from meinberlin.apps.moderationtasks.filters import OpenTaskFilter
from meinberlin.apps.moderationtasks.models import ModerationTask
from meinberlin.apps.moderatorfeedback.models import (
    DEFAULT_CHOICES as moderator_status_default_choices,
)


class ProposalFilterSet(DefaultsRestFilterSet):
    is_archived = rest_filters.BooleanFilter()
    category = rest_filters.ModelChoiceFilter(queryset=Category.objects.all())
    labels = rest_filters.ModelChoiceFilter(queryset=Label.objects.all())
    moderator_status = rest_filters.ChoiceFilter(
        choices=moderator_status_default_choices
    )
    open_task = OpenTaskFilter(queryset=ModerationTask.objects.all())

    defaults = {"is_archived": "false"}


class ProposalFilterBackend(rest_filters.DjangoFilterBackend):
    """Use with ProposalFilterSet.

    Set filterset_class = ProposalFilterSet in the view that uses this
    filter backend.
    """

    # do not raise exceptions for invalid filter values
    raise_exception = False
