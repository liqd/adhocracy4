from django.utils.translation import gettext_lazy as _
from wagtail.core import blocks

from adhocracy4.actions.models import Action


class PlatformActivityBlock(blocks.StructBlock):
    heading = blocks.CharBlock(label=_('Heading'))
    count = blocks.IntegerBlock(label=_('Count'), default=5)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        block = context['self']
        context['actions'] = Action.objects \
            .filter_public().exclude_updates()[:block['count']]
        return context

    class Meta:
        template = 'meinberlin_actions/blocks/platform_activity_block.html'
        icon = 'time'
