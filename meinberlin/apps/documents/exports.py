from django.utils.translation import ugettext as _
from rules.contrib.views import PermissionRequiredMixin

from adhocracy4.comments.models import Comment
from adhocracy4.exports import mixins
from adhocracy4.exports import views as export_views


class DocumentExportView(
        PermissionRequiredMixin,
        mixins.ExportModelFieldsMixin,
        mixins.UserGeneratedContentExportMixin,
        mixins.ItemExportWithLinkMixin,
        mixins.ItemExportWithRatesMixin,
        mixins.CommentExportWithRepliesToMixin,
        export_views.BaseItemExportView
):

    model = Comment
    permission_required = 'a4projects.change_project'

    fields = ['id', 'comment', 'created']

    def get_permission_object(self):
        return self.module.project

    def get_queryset(self):
        comments = (
            Comment.objects.filter(paragraph__chapter__module=self.module) |
            Comment.objects.filter(chapter__module=self.module) |
            Comment.objects.filter(
                parent_comment__paragraph__chapter__module=self.module) |
            Comment.objects.filter(parent_comment__chapter__module=self.module)
        )
        return comments

    def get_virtual_fields(self, virtual):
        virtual.setdefault('id', _('ID'))
        virtual.setdefault('comment', _('Comment'))
        virtual.setdefault('created', _('Created'))
        return super().get_virtual_fields(virtual)

    @property
    def raise_exception(self):
        return self.request.user.is_authenticated
