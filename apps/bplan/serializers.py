from django.apps import apps
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from rest_framework import serializers

from adhocracy4.modules import models as module_models
from adhocracy4.phases import models as phase_models

from .models import Bplan
from .phases import StatementPhase


BPLAN_EMBED = '<iframe height="500" style="width: 100%; min-height: 300px; ' \
              'max-height: 100vh" src="{}" frameborder="0"></iframe>'


class BplanSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    typ = serializers.HiddenField(default='Bplan')
    is_draft = serializers.HiddenField(default=False)

    # write_only as not part of the model
    start_date = serializers.DateTimeField(write_only=True)
    end_date = serializers.DateTimeField(write_only=True)

    class Meta:
        model = Bplan
        fields = (
            'id', 'name', 'description', 'is_archived', 'url',
            'office_worker_email', 'typ', 'is_draft', 'start_date',
            'end_date'
        )

    def create(self, validated_data):
        orga_pk = self._context.get('organisation_pk', None)
        orga_model = apps.get_model(settings.A4_ORGANISATIONS_MODEL)
        orga = orga_model.objects.get(pk=orga_pk)
        validated_data['organisation'] = orga
        start_date = validated_data.pop('start_date')
        end_date = validated_data.pop('end_date')
        bplan = super().create(validated_data)
        self._create_module_and_phase(bplan, start_date, end_date)
        return bplan

    def _create_module_and_phase(self, bplan, start_date, end_date):
        module = module_models.Module.objects.create(
            name=bplan.slug + '_module',
            weight=1,
            project=bplan,
        )

        phase_content = StatementPhase()
        phase_models.Phase.objects.create(
            name=_('Bplan statement phase'),
            description=_('Bplan statement phase'),
            type=phase_content.identifier,
            module=module,
            start_date=start_date,
            end_date=end_date
        )

    def to_representation(self, instance):
        dict = super().to_representation(instance)
        dict['embed_code'] = self._response_embed_code(instance)
        return dict

    def _response_embed_code(self, bplan):
        url = self._get_absolute_url(bplan)
        embed = BPLAN_EMBED.format(url)
        return embed

    def _get_absolute_url(self, bplan):
        site_url = Site.objects.get_current().domain
        embed_url = reverse('embed-project', kwargs={'slug': bplan.slug, })
        url = 'https://{}{}'.format(site_url, embed_url)
        return url
