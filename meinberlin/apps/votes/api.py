from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from adhocracy4.api.permissions import ViewSetRulesPermission
from adhocracy4.modules.models import Module

from .models import TokenVote
from .models import VotingToken
from .serializers import TokenVoteSerializer
from .serializers import VotingTokenSerializer


class VotingTokenInfoMixin:
    """Adds token info to response data of an api list view.

    Needs to be used with rest_framework.mixins.ListModelMixin
    """

    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        token_info = None
        if 'voting_token' in request.session:
            try:
                token = VotingToken.objects.get(
                    pk=request.session['voting_token']
                )
            except VotingToken.DoesNotExist:
                pass
            serializer = VotingTokenSerializer(token)
            token_info = serializer.data

        response.data['token_info'] = token_info
        return response


class TokenVoteMixin:
    """Should be used in combination with TokenVoteRouter.

    Adds module, content_type_id and token to api view.
    """

    def dispatch(self, request, *args, **kwargs):
        self.module_pk = kwargs.get('module_pk', '')
        self.content_type_id = kwargs.get('content_type', '')
        try:
            session = Session.objects.get(pk=request.session.session_key)
            token_id = session.get_decoded()['voting_token']
            self.token = VotingToken.objects.get(pk=token_id)
        except ObjectDoesNotExist:
            pass
        except KeyError:
            pass

        return super().dispatch(request, *args, **kwargs)

    @property
    def module(self):
        return get_object_or_404(
            Module,
            pk=self.module_pk
        )

    @property
    def content_type(self):
        try:
            return ContentType.objects.get_for_id(self.content_type_id)
        except ContentType.DoesNotExist:
            raise Http404

    def check_permissions(self, request):
        """Check if valid token is there before checking other permissions."""
        if not hasattr(self, 'token'):
            self.permission_denied(
                request,
                message=_('No token given.')
            )
        elif not self.token.is_active:
            self.permission_denied(
                request,
                message=_('Token is inactive.')
            )
        elif not self.token.module == self.module:
            self.permission_denied(
                request,
                message=_('Token not valid for module.')
            )

        super().check_permissions(request)


class TokenVotePermission(BasePermission):
    """Needs to be used in combination with TokenVoteMixin."""

    def has_permission(self, request, view):
        if view.action == 'create':
            return view.token.has_votes_left
        elif view.action == 'destroy':
            vote = view.get_object()
            return vote.token == view.token
        else:
            return False


class TokenVoteViewSet(mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       TokenVoteMixin,
                       viewsets.GenericViewSet):
    """Api view to create or delete token votes.

    Uses 2 permission classes:
        - ViewSetRulesPermission: create  -> {app_label}.add_vote
                                  destroy -> {app_label}.delete_vote

                                  both of these permissions need to be
                                  implemented in the app that it is
                                  used with (see e.g. meinberlin_budgeting)

        - TokenVotePermission: does not use user based rules, but
                               instead checks that token is valid
                               for respective action
    """

    serializer_class = TokenVoteSerializer
    permission_classes = (ViewSetRulesPermission, TokenVotePermission)
    lookup_field = 'object_pk'

    def get_queryset(self):
        return TokenVote.objects.filter(token=self.token,
                                        content_type=self.content_type)

    def get_permission_object(self):
        # for voting, the permission object is the item that is voted on
        if self.action == 'create':
            return self.content_type.get_object_for_this_type(
                pk=self.request.data['object_id']
            )
        else:
            return self.token.module

    @property
    def rules_method_map(self):
        return ViewSetRulesPermission.default_rules_method_map._replace(
            POST='{app_label}.vote_{model}'.format(
                app_label=self.content_type.app_label,
                model=self.content_type.model),
            DELETE='{app_label}.delete_vote'.format(
                app_label=self.content_type.app_label)
        )

    def create(self, request, *args, **kwargs):
        data = {'token': self.token.pk,
                'content_type': self.content_type_id,
                'object_pk': request.data['object_id']}

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)
