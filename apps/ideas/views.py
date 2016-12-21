from django.views import generic
from rules.contrib.views import PermissionRequiredMixin

from adhocracy4.projects import mixins

from . import models as idea_models


class IdeaListView(mixins.ProjectMixin, generic.ListView):
    model = idea_models.Idea


class IdeaDetailView(PermissionRequiredMixin, generic.DetailView):
    model = idea_models.Idea
    queryset = idea_models.Idea.objects.annotate_positive_rating_count()\
                                       .annotate_negative_rating_count()
    permission_required = 'meinberlin_ideas.view_idea'

    @property
    def raise_exception(self):
        return self.request.user.is_authenticated()
