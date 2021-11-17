from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from adhocracy4.api.mixins import ModuleMixin
from adhocracy4.api.permissions import ViewSetRulesPermission

from .models import Proposal
from .serializers import ProposalSerializer


# To be changed to a more general IdeaPagination, when using
# pagination via rest api for more idea lists
class BudgetPagination(PageNumberPagination):
    page_size = 15

    def get_next_page(self):
        if self.page.has_next():
            return self.page.next_page_number()
        else:
            return None

    def get_previous_page(self):
        if self.page.has_previous():
            return self.page.previous_page_number()
        else:
            return None

    def get_paginated_response(self, data):
        return Response({
            'status': True,
            'results': data,
            'meta': {
                'results_count': self.page.paginator.count,
                'current_page': self.page.number,
                'previous_page': self.get_previous_page(),
                'next_page': self.get_next_page(),
                'page_count': self.page.paginator.num_pages,
                'page_size': self.page_size,
                'is_paginated': self.page.paginator.num_pages > 1
            }},
            status=status.HTTP_200_OK)


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
