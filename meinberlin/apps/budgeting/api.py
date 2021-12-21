from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination

from adhocracy4.api.mixins import ModuleMixin
from adhocracy4.api.permissions import ViewSetRulesPermission
from adhocracy4.categories import get_category_icon_url
from adhocracy4.categories import has_icons
from adhocracy4.categories.models import Category
from meinberlin.apps.contrib.filters import IdeaCategoryFilterBackend
from meinberlin.apps.votes.api import VotingTokenInfoMixin

from .models import Proposal
from .serializers import ProposalSerializer


# To be changed to a more general IdeaPagination, when using
# pagination via rest api for more idea lists
class ProposalPagination(PageNumberPagination):
    page_size = 15

    def get_paginated_response(self, data):
        response = super(ProposalPagination, self).get_paginated_response(data)
        response.data['page_size'] = self.page_size
        response.data['page_count'] = self.page.paginator.num_pages
        return response


class LocaleInfoMixin:
    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        response.data['locale'] = get_language()
        return response


class ProposalFilterInfoMixin(ModuleMixin):
    def list(self, request, *args, **kwargs):
        """Add the filter information to the data of the Proposal API.

        Needs to be used with rest_framework.mixins.ListModelMixin
        """
        filters = {}

        ordering_choices = [('-created', _('Most recent')), ]
        if self.module.has_feature('rate', Proposal):
            ordering_choices += ('-positive_rating_count', _('Most popular')),
        ordering_choices += ('-comment_count', _('Most commented')),

        filters['ordering'] = {
            'label': _('Ordering'),
            'choices': ordering_choices,
            'default': '-created',
        }

        categories = Category.objects.filter(
            module=self.module
        )
        if categories:
            category_choices = [('', _('All')), ]
            if has_icons(self.module):
                category_icons = []
            for category in categories:
                category_choices += (str(category.pk), category.name),
                if has_icons(self.module):
                    icon_name = getattr(category, 'icon', None)
                    icon_url = get_category_icon_url(icon_name)
                    category_icons += (str(category.pk), icon_url),

            filters['category'] = {
                'label': _('Category'),
                'choices': category_choices,
            }
            if has_icons(self.module):
                filters['category']['icons'] = category_icons

        filters['is_archived'] = {
            'label': _('Archived'),
            'choices': [
                ('', _('All')),
                ('false', _('No')),
                ('true', _('Yes')),
            ],
            'default': 'false',
        }

        response = super().list(request, args, kwargs)
        response.data['filters'] = filters
        return response


class ProposalViewSet(ProposalFilterInfoMixin,
                      LocaleInfoMixin,
                      VotingTokenInfoMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet,
                      ):

    pagination_class = ProposalPagination
    serializer_class = ProposalSerializer
    permission_classes = (ViewSetRulesPermission,)
    filter_backends = (DjangoFilterBackend,
                       OrderingFilter,
                       IdeaCategoryFilterBackend,)
    filter_fields = ('is_archived', 'category',)
    ordering_fields = ('created',
                       'comment_count',
                       'positive_rating_count',)

    def get_permission_object(self):
        return self.module

    def get_queryset(self):
        proposals = Proposal.objects\
            .filter(module=self.module) \
            .annotate_comment_count() \
            .annotate_positive_rating_count() \
            .annotate_negative_rating_count() \
            .order_by('-created')
        return proposals
