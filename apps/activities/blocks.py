from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailcore import blocks

from .models import Activity


class PlatformActivityBlock(blocks.StructBlock):
    heading = blocks.CharBlock(label=_('Heading'))
    count = blocks.IntegerBlock(label=_('Count'), default=5)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        block = context['self']
        context['activities'] = Activity.objects.all()[:block['count']]
        return context

    class Meta:
        template = 'meinberlin_activities/blocks/platform_activity_block.html'
        icon = 'time'
