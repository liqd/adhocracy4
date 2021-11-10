from rest_framework import mixins
from rest_framework import viewsets

from adhocracy4.api.mixins import ModuleMixin
from adhocracy4.api.permissions import ViewSetRulesPermission

from .models import Proposal
from .serializers import ProposalSerializer


class ProposalViewSet(ModuleMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet,
                      ):

    serializer_class = ProposalSerializer
    permission_classes = (ViewSetRulesPermission,)

    def get_permission_object(self):
        return self.module

    def get_queryset(self):
        proposals = Proposal.objects\
            .filter(module=self.module) \
            .annotate_comment_count() \
            .annotate_positive_rating_count() \
            .annotate_negative_rating_count() \
            .order_by('created')
        return proposals
