from rest_framework.filters import BaseFilterBackend

from meinberlin.apps.votes.models import TokenVote
from meinberlin.apps.votes.models import VotingToken


class OwnVotesFilterBackend(BaseFilterBackend):
    """Filter items for own votes."""

    def filter_queryset(self, request, queryset, view):

        if "own_votes" in request.GET:
            own_votes = request.GET["own_votes"]
            if own_votes:
                if "voting_tokens" in request.session:
                    module_key = str(view.module.id)
                    if module_key in request.session["voting_tokens"]:
                        token = None
                        try:
                            token = VotingToken.objects.get(
                                token=request.session["voting_tokens"][module_key],
                                module=view.module,
                            )
                        except VotingToken.DoesNotExist:
                            pass

                        if token:
                            own_votes = TokenVote.objects.filter(token=token)
                            return queryset.filter(id__in=own_votes.values("object_pk"))
                return queryset.none()
        return queryset
