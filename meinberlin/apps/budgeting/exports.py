from django.utils.translation import ugettext_lazy as _

from meinberlin.apps.exports import views as export_views
from meinberlin.apps.exports import register_export

from . import models


@register_export(_('Proposals with comments'))
class ProposalExportView(export_views.ItemExportView,
                         export_views.ItemExportWithRatesMixin,
                         export_views.ItemExportWithCommentCountMixin,
                         export_views.ItemExportWithCommentsMixin,
                         export_views.ItemExportWithLocationMixin,
                         export_views.ItemExportWithModeratorFeedback):
    model = models.Proposal
    fields = ['name', 'description', 'creator', 'created', 'budget']

    def get_queryset(self):
        return super().get_queryset() \
            .filter(module=self.module)\
            .annotate_comment_count()\
            .annotate_positive_rating_count()\
            .annotate_negative_rating_count()
