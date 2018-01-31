from django.utils.translation import ugettext_lazy as _

from adhocracy4.exports import mixins as a4_export_mixins
from adhocracy4.exports import views as a4_export_views
from meinberlin.apps.exports import mixins as export_mixins
from meinberlin.apps.exports import register_export
from meinberlin.apps.exports.views import ItemExportWithModeratorFeedback

from . import models


@register_export(_('Proposals with comments'))
class ProposalExportView(a4_export_views.ItemExportView,
                         export_mixins.ItemExportWithReferenceNumberMixin,
                         a4_export_mixins.ItemExportWithRatesMixin,
                         a4_export_mixins.ItemExportWithCommentCountMixin,
                         a4_export_mixins.ItemExportWithCommentsMixin,
                         a4_export_mixins.ItemExportWithLocationMixin,
                         a4_export_mixins.ItemExportWithCategoriesMixin,
                         ItemExportWithModeratorFeedback):
    model = models.Proposal
    fields = ['name', 'description', 'creator', 'created', 'budget']

    def get_queryset(self):
        return super().get_queryset() \
            .filter(module=self.module)\
            .annotate_comment_count()\
            .annotate_positive_rating_count()\
            .annotate_negative_rating_count()
