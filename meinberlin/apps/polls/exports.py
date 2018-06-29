from django.utils import timezone
from django.utils.translation import ugettext as _

from adhocracy4.comments.models import Comment
from adhocracy4.exports import mixins as export_mixins
from adhocracy4.exports import views as export_views
from meinberlin.apps.exports import mixins as mb_export_mixins
from meinberlin.apps.exports import register_export


@register_export(_('Comments of Polls'))
class PollExportView(
        export_mixins.ExportModelFieldsMixin,
        mb_export_mixins.UserGeneratedContentExportMixin,
        export_mixins.ItemExportWithLinkMixin,
        mb_export_mixins.ItemExportWithRepliesToMixin,
        export_views.BaseItemExportView
):

    model = Comment

    fields = ['id', 'comment', 'created']

    def get_queryset(self):
        comments = (
            Comment.objects.filter(poll__module=self.module) |
            Comment.objects.filter(parent_comment__poll__module=self.module)
        )
        return comments

    def get_base_filename(self):
        return '%s_%s' % (self.project.slug,
                          timezone.now().strftime('%Y%m%dT%H%M%S'))

    def get_virtual_fields(self, virtual):
        virtual.setdefault('id', _('ID'))
        virtual.setdefault('comment', _('Comment'))
        virtual.setdefault('created', _('Created'))
        return super().get_virtual_fields(virtual)
