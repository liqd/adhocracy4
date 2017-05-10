import os

from urllib import request
from urllib.parse import urlparse

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

PROJECT_IMAGE_DIR = 'projects/backgrounds/'


class BplanSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    typ = serializers.HiddenField(default='Bplan')

    # make write_only for consistency  reasons
    start_date = serializers.DateTimeField(write_only=True)
    end_date = serializers.DateTimeField(write_only=True)
    image_url = serializers.URLField(required=False, write_only=True)

    class Meta:
        model = Bplan
        fields = (
            'id', 'name', 'description', 'url', 'office_worker_email', 'typ',
            'is_draft', 'start_date', 'end_date', 'image_url'
        )
        extra_kwargs = {
            # write_only for constency reasons
            'is_draft': {'default': False, 'write_only': True},
            'name': {'write_only': True},
            'description': {'write_only': True},
            'url': {'write_only': True},
            'office_worker_email': {'write_only': True}
        }

    def create(self, validated_data):
        orga_pk = self._context.get('organisation_pk', None)
        orga_model = apps.get_model(settings.A4_ORGANISATIONS_MODEL)
        orga = orga_model.objects.get(pk=orga_pk)
        validated_data['organisation'] = orga

        start_date = validated_data.pop('start_date')
        end_date = validated_data.pop('end_date')

        image_url = validated_data.pop('image_url', None)
        if image_url:
            try:
                validated_data['image'] = \
                    self._download_image_from_url(image_url)
            except:
                raise serializers.ValidationError(
                    'Failed to download image {}'.format(image_url))

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

    def _download_image_from_url(self, url):
        parsed_url = urlparse(url)
        file_path = PROJECT_IMAGE_DIR + os.path.basename(parsed_url.path)
        file_name = settings.MEDIA_ROOT + '/' + file_path
        request.urlretrieve(url, file_name)
        return file_path
