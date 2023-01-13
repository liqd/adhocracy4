import rules

from meinberlin.apps.livequestions.models import LiveQuestion

from .predicates import phase_allows_like
from .predicates import phase_allows_like_model

rules.add_perm("meinberlin_likes.add_like", phase_allows_like)

rules.add_perm("meinberlin_likes.add_like_model", phase_allows_like_model(LiveQuestion))
