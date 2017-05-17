from apps.mapideas.forms import MapIdeaForm

from . import models


class ProposalForm(MapIdeaForm):

    class Meta:
        model = models.Proposal
        fields = ['name', 'description', 'category', 'budget',
                  'creator_contribution', 'point', 'point_label']
