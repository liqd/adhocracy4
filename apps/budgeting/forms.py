from apps.mapideas.forms import MapIdeaForm

from apps.moderatorfeedback.forms import item_moderate_form_factory

from . import models


class ProposalForm(MapIdeaForm):

    class Meta:
        model = models.Proposal
        fields = ['name', 'description', 'category', 'budget', 'point',
                  'point_label']


ProposalModerateForm = item_moderate_form_factory(models.Proposal)
