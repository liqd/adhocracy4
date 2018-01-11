from django.utils.translation import ugettext_lazy as _

from adhocracy4.exports import mixins as export_mixins
from adhocracy4.exports import views as export_views
from meinberlin.apps.exports import register_export

from . import models


@register_export(_('Ideas with comments'))
class IdeaExportView(export_views.ItemExportView,
                     export_mixins.ItemExportWithRatesMixin,
                     export_mixins.ItemExportWithCommentCountMixin,
                     export_mixins.ItemExportWithCategoriesMixin,
                     export_mixins.ItemExportWithCommentsMixin):
    model = models.Idea
    fields = ['name', 'description', 'creator', 'created']

    def get_queryset(self):
        return super().get_queryset() \
            .filter(module=self.module)\
            .annotate_comment_count()\
            .annotate_positive_rating_count()\
            .annotate_negative_rating_count()
