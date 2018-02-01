from django.utils.translation import ugettext as _

from adhocracy4.exports.mixins import VirtualFieldMixin


class ItemExportWithReferenceNumberMixin(VirtualFieldMixin):

    def get_virtual_fields(self, virtual):
        if 'reference_number' not in virtual:
            virtual['reference_number'] = _('Reference Number')
        return super().get_virtual_fields(virtual)

    def get_reference_number_data(self, item):
        if hasattr(item, 'reference_number'):
            return item.reference_number
        return ''
