from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from adhocracy4.comments.models import Comment
from adhocracy4.exports import mixins as export_mixins
from adhocracy4.exports import views as export_views
from adhocracy4.projects.mixins import ProjectMixin
from meinberlin.apps.exports import register_export


class ItemExportWithCommentUserMixin(export_mixins.VirtualFieldMixin):
    def get_virtual_fields(self, virtual):
        virtual['user'] = 'user'
        return super().get_virtual_fields(virtual)

    def get_user_data(self, item):
        return item.creator.username


class ItemExportWithRepliesToMixin(export_mixins.VirtualFieldMixin):
    def get_virtual_fields(self, virtual):
        virtual['replies_to'] = 'replies_to'
        return super().get_virtual_fields(virtual)

    def get_replies_to_data(self, comment):
        try:
            return comment.parent_comment.get().pk
        except Comment.DoesNotExist:
            return ''


@register_export(_('Documents with comments'))
class DocumentExportView(
        export_views.BaseItemExportView, export_mixins.ExportModelFieldsMixin,
        export_mixins.ItemExportWithLinkMixin,
        export_mixins.ItemExportWithRatesMixin, ItemExportWithCommentUserMixin,
        ItemExportWithRepliesToMixin, ProjectMixin):
    def get_base_filename(self):
        return '%s_%s' % (self.project.slug,
                          timezone.now().strftime('%Y%m%dT%H%M%S'))

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
