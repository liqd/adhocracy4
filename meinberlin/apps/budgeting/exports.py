from django.utils.translation import ugettext as _
from rules.contrib.views import PermissionRequiredMixin

from adhocracy4.comments.models import Comment
from adhocracy4.exports import mixins
from adhocracy4.exports import views as a4_export_views

from . import models


class ProposalExportView(PermissionRequiredMixin,
                         mixins.ItemExportWithReferenceNumberMixin,
                         mixins.ItemExportWithLinkMixin,
                         mixins.ExportModelFieldsMixin,
                         mixins.ItemExportWithRatesMixin,
                         mixins.ItemExportWithCategoriesMixin,
                         mixins.ItemExportWithLabelsMixin,
                         mixins.ItemExportWithCommentCountMixin,
                         mixins.ItemExportWithLocationMixin,
                         mixins.UserGeneratedContentExportMixin,
                         mixins.ItemExportWithModeratorFeedback,
                         mixins.ItemExportWithModeratorRemark,
                         a4_export_views.BaseItemExportView):
    model = models.Proposal
    fields = ['name', 'description', 'budget', 'contact_email',
              'contact_phone']
    html_fields = ['description']
    permission_required = 'a4projects.change_project'

    def get_permission_object(self):
        return self.module.project

    def get_queryset(self):
        return super().get_queryset() \
            .filter(module=self.module)\
            .annotate_comment_count()\
            .annotate_positive_rating_count()\
            .annotate_negative_rating_count()

    def get_virtual_fields(self, virtual):
        virtual = super().get_virtual_fields(virtual)
        virtual['contact_email'] = _('Contact E-Mail')
        virtual['contact_phone'] = _('Contact Phone')
        return virtual

    @property
    def raise_exception(self):
        return self.request.user.is_authenticated


class ProposalCommentExportView(
        PermissionRequiredMixin,
        mixins.ExportModelFieldsMixin,
        mixins.UserGeneratedContentExportMixin,
        mixins.ItemExportWithLinkMixin,
        mixins.ItemExportWithRatesMixin,
        mixins.CommentExportWithRepliesToMixin,
        mixins.CommentExportWithRepliesToReferenceMixin,
        a4_export_views.BaseItemExportView):

    model = Comment

    fields = ['id', 'comment', 'created']
    permission_required = 'a4projects.change_project'

    def get_permission_object(self):
        return self.module.project

    def get_queryset(self):
        comments = (Comment.objects.filter(
                    budget_proposal__module=self.module) |
                    Comment.objects.filter(
                    parent_comment__budget_proposal__module=self.module)
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
