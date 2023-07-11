from django.utils.translation import gettext as _

from adhocracy4.categories.models import CategoryAlias
from adhocracy4.exports import unescape_and_strip_html
from adhocracy4.labels.models import LabelAlias

from .base import VirtualFieldMixin


class ItemExportWithCategoriesMixin(VirtualFieldMixin):
    """
    Adds the category to an item.
    """

    def get_virtual_fields(self, virtual):
        if "category" not in virtual:
            if hasattr(self, "module") and CategoryAlias.get_category_alias(
                self.module
            ):
                virtual["category"] = CategoryAlias.get_category_alias(
                    self.module
                ).title
            else:
                virtual["category"] = _("Category")
        return super().get_virtual_fields(virtual)

    def get_category_data(self, item):
        if hasattr(item, "category") and item.category:
            return item.category.name
        return ""


class ItemExportWithLabelsMixin(VirtualFieldMixin):
    """
    Adds the labels to an item.
    """

    def get_virtual_fields(self, virtual):
        if "labels" not in virtual:
            if hasattr(self, "module") and LabelAlias.get_label_alias(self.module):
                virtual["labels"] = LabelAlias.get_label_alias(self.module).title
            else:
                virtual["labels"] = _("Labels")
        return super().get_virtual_fields(virtual)

    def get_labels_data(self, item):
        if hasattr(item, "labels") and item.labels:
            return ", ".join(item.labels.all().values_list("name", flat=True))
        return ""


class ItemExportWithReferenceNumberMixin(VirtualFieldMixin):
    """
    Adds the reference number to an item.

    Only to be used with items that have a reference number.
    """

    def get_virtual_fields(self, virtual):
        if "reference_number" not in virtual:
            virtual["reference_number"] = _("Reference No.")
        return super().get_virtual_fields(virtual)

    def get_reference_number_data(self, item):
        if hasattr(item, "reference_number"):
            return item.reference_number
        return ""


class ItemExportWithModeratorFeedback(VirtualFieldMixin):
    """
    Adds moderator feedback to an item.

    Only to be used in projects that have moderator feedback implemented (see
    https://github.com/liqd/adhocracy-plus/tree/main/apps/moderatorfeedback)
    And only with items that use it.
    """

    def get_virtual_fields(self, virtual):
        if "moderator_status" not in virtual:
            virtual["moderator_status"] = _("Status")
        if "moderator_feedback_text" not in virtual:
            virtual["moderator_feedback_text"] = _("Feedback")
        return super().get_virtual_fields(virtual)

    def get_moderator_status_data(self, item):
        return item.get_moderator_status_display()

    def get_moderator_feedback_text_data(self, item):
        if item.moderator_feedback_text:
            feedback_text = item.moderator_feedback_text.feedback_text
            return unescape_and_strip_html(feedback_text)
        return ""


class ItemExportWithModeratorRemark(VirtualFieldMixin):
    """
    Adds moderator remarks to an item.

    Only to be used in projects that have moderator remarks implemented (see
    https://github.com/liqd/adhocracy-plus/tree/main/apps/moderatorremark)
    And only with items that use it.
    """

    def get_virtual_fields(self, virtual):
        if "moderator_remark" not in virtual:
            virtual["moderator_remark"] = _("Remark")
        return super().get_virtual_fields(virtual)

    def get_moderator_remark_data(self, item):
        remark = item.remark
        if remark:
            return unescape_and_strip_html(remark.remark)
        return ""
