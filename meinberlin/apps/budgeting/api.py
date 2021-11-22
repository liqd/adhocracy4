from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from adhocracy4.api.mixins import ModuleMixin
from adhocracy4.api.permissions import ViewSetRulesPermission

from .models import Proposal
from .serializers import ProposalSerializer


# To be changed to a more general IdeaPagination, when using
# pagination via rest api for more idea lists
class BudgetPagination(PageNumberPagination):
    page_size = 15

    def get_paginated_response(self, data):
        response = super(BudgetPagination, self).get_paginated_response(data)
        response.data['page_size'] = self.page_size
        response.data['page_count'] = self.page.paginator.num_pages
        return response


class ProposalViewSet(ModuleMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet,
                      ):

    pagination_class = BudgetPagination
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
