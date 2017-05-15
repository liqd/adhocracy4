import os
from urllib import request
from urllib.parse import urlparse

from django.apps import apps
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.files.images import ImageFile
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from rest_framework import serializers

from adhocracy4.images.validators import validate_image
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
            validated_data['image'] = \
                self._download_image_from_url(image_url)

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

    def update(self, instance, validated_data):
        start_date = validated_data.pop('start_date', None)
        end_date = validated_data.pop('end_date', None)
        if start_date or end_date:
            self._update_phase(instance, start_date, end_date)

        image_url = validated_data.pop('image_url', None)
        if image_url:
            validated_data['image'] = \
                self._download_image_from_url(image_url)

        return super().update(instance, validated_data)

    def _update_phase(self, bplan, start_date, end_date):
        module = module_models.Module.objects.get(project=bplan)
        phase = phase_models.Phase.objects.get(module=module)
        if start_date:
            phase.start_date = start_date
        if end_date:
            phase.end_date = end_date
        phase.save()

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
        try:
            parsed_url = urlparse(url)
            file_path = os.path.join(PROJECT_IMAGE_DIR,
                                     os.path.basename(parsed_url.path))
            file_name = os.path.join(settings.MEDIA_ROOT, file_path)
            file_dir = os.path.dirname(file_name)
            os.makedirs(file_dir, exist_ok=True)

            request.urlretrieve(url, file_name)
            self._validate_image(file_name)
        except ValidationError as e:
            self._remove_image_if_exists(file_name)
            raise serializers.ValidationError(e)
        except:
            self._remove_image_if_exists(file_name)
            raise serializers.ValidationError(
                'Failed to download image {}'.format(url))
        return file_path

    def _validate_image(self, file_name):
        image_file = open(file_name, "rb")
        image = ImageFile(image_file, file_name)
        config = settings.IMAGE_ALIASES.get('*', {})
        config.update(settings.IMAGE_ALIASES['heroimage'])
        validate_image(image, **config)

    def _remove_image_if_exists(self, file_name):
        try:
            os.remove(file_name)
        except:
            pass
