import django_filters
from django.utils.translation import ugettext_lazy as _

from adhocracy4.filters.widgets import DropdownLinkWidget

from . import mixins


class OrderingWidget(DropdownLinkWidget):
    label = _('Ordering')
    right = True


class OrderingFilter(mixins.ChoicesRequestMixin,
                     django_filters.OrderingFilter):

    def __init__(self, *args, **kwargs):
        if 'widget' not in kwargs:
            kwargs['widget'] = OrderingWidget
        kwargs['empty_label'] = None
        super().__init__(*args, **kwargs)
