from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from adhocracy4.comments.models import Comment
from adhocracy4.exports import mixins as export_mixins
from adhocracy4.exports import views as export_views
from meinberlin.apps.exports import mixins as mb_export_mixins
from meinberlin.apps.exports import register_export


@register_export(_('Documents with comments'))
class DocumentExportView(
        export_mixins.ExportModelFieldsMixin,
        mb_export_mixins.UserGeneratedContentExportMixin,
        export_mixins.ItemExportWithLinkMixin,
        export_mixins.ItemExportWithRatesMixin,
        mb_export_mixins.ItemExportWithRepliesToMixin,
        export_views.BaseItemExportView
):

    model = Comment

    fields = ['id', 'comment', 'created']

    def get_queryset(self):
        comments = (
            Comment.objects.filter(paragraph__chapter__module=self.module) |
            Comment.objects.filter(chapter__module=self.module) |
            Comment.objects.filter(
                parent_comment__paragraph__chapter__module=self.module) |
            Comment.objects.filter(parent_comment__chapter__module=self.module)
        )
        return comments

    def get_base_filename(self):
        return '%s_%s' % (self.project.slug,
                          timezone.now().strftime('%Y%m%dT%H%M%S'))
