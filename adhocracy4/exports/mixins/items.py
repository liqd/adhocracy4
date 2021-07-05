from django.utils.translation import ugettext as _

from .base import VirtualFieldMixin


class ItemExportWithCategoriesMixin(VirtualFieldMixin):
    """
    Adds the category to an item.
    """
    def get_virtual_fields(self, virtual):
        if 'category' not in virtual:
            virtual['category'] = _('Category')
        return super().get_virtual_fields(virtual)

    def get_category_data(self, item):
        if hasattr(item, 'category') and item.category:
            return item.category.name
        return ''


class ItemExportWithLabelsMixin(VirtualFieldMixin):
    """
    Adds the labels to an item.
    """
    def get_virtual_fields(self, virtual):
        if 'labels' not in virtual:
            virtual['labels'] = _('Labels')
        return super().get_virtual_fields(virtual)

    def get_labels_data(self, item):
        if hasattr(item, 'labels') and item.labels:
            return ', '.join(item.labels.all().values_list('name', flat=True))
        return ''
