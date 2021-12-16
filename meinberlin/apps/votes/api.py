from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from adhocracy4.api.permissions import ViewSetRulesPermission

from .models import TokenVote
from .models import VotingToken
from .serializers import TokenVoteSerializer


class TokenVoteMixin:
    """Should be used in combination with TokenVoteRouter.

    Adds content_type_id and token to api view
    """

    def dispatch(self, request, *args, **kwargs):
        content_type = kwargs.get('content_type', '')
        if not content_type.isdigit():
            raise Http404
        else:
            self.content_type_id = int(content_type)

        try:
            session = Session.objects.get(pk=request.session.session_key)
            token_id = session.get_decoded()['voting_token']
            self.token = VotingToken.objects.get(pk=token_id)
        except ObjectDoesNotExist:
            raise PermissionDenied('No Token given')

        return super().dispatch(request, *args, **kwargs)

    @property
    def content_type(self):
        try:
            return ContentType.objects.get_for_id(self.content_type_id)
        except ContentType.DoesNotExist:
            raise Http404


class TokenVoteViewSet(mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       TokenVoteMixin,
                       viewsets.GenericViewSet):

    serializer_class = TokenVoteSerializer
    permission_classes = (ViewSetRulesPermission,)
    lookup_field = 'object_pk'

    def get_queryset(self):
        return TokenVote.objects.filter(token=self.token)

    def get_permission_object(self):
        return self.token.module

    @property
    def rules_method_map(self):
        return ViewSetRulesPermission.default_rules_method_map._replace(
            POST='{app_label}.vote_{model}'.format(
                app_label=self.content_type.app_label,
                model=self.content_type.model
            )
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
