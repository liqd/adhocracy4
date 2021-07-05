from django.utils.translation import ugettext as _
from rules.contrib.views import PermissionRequiredMixin

from adhocracy4.comments.models import Comment
from adhocracy4.exports import mixins
from adhocracy4.exports import views as export_views


class PollCommentExportView(
        PermissionRequiredMixin,
        mixins.ExportModelFieldsMixin,
        mixins.UserGeneratedContentExportMixin,
        mixins.ItemExportWithLinkMixin,
        mixins.CommentExportWithRepliesToMixin,
        export_views.BaseItemExportView
):

    model = Comment

    fields = ['id', 'comment', 'created']
    permission_required = 'a4projects.change_project'

    def get_permission_object(self):
        return self.module.project

    def get_queryset(self):
        comments = (
            Comment.objects.filter(poll__module=self.module) |
            Comment.objects.filter(parent_comment__poll__module=self.module)
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
