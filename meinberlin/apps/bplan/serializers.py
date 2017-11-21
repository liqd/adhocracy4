import datetime
import posixpath
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
from adhocracy4.projects import models as project_models
from meinberlin.apps.dashboard2 import signals as a4dashboard_signals
from meinberlin.apps.dashboard2 import components

from .models import Bplan
from .phases import StatementPhase

BPLAN_EMBED = '<iframe height="500" style="width: 100%; min-height: 300px; ' \
              'max-height: 100vh" src="{}" frameborder="0"></iframe>'


class BplanSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    # make write_only for consistency  reasons
    start_date = serializers.DateTimeField(write_only=True)
    end_date = serializers.DateTimeField(write_only=True)
    image_url = serializers.URLField(required=False, write_only=True)
    image_copyright = serializers.CharField(required=False, write_only=True,
                                            source='tile_image_copyright',
                                            allow_blank=True,
                                            max_length=120)
    embed_code = serializers.SerializerMethodField()

    class Meta:
        model = Bplan
        fields = (
            'id', 'name', 'description', 'url', 'office_worker_email',
            'is_draft', 'start_date', 'end_date', 'image_url',
            'image_copyright', 'embed_code'
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
            validated_data['tile_image'] = \
                self._download_image_from_url(image_url)

        bplan = super().create(validated_data)
        self._create_module_and_phase(bplan, start_date, end_date)
        self._send_project_created_signal(bplan)
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
            validated_data['tile_image'] = \
                self._download_image_from_url(image_url)

        instance = super().update(instance, validated_data)
        self._send_component_updated_signal(instance)
        return instance

    def _update_phase(self, bplan, start_date, end_date):
        module = module_models.Module.objects.get(project=bplan)
        phase = phase_models.Phase.objects.get(module=module)
        if start_date:
            phase.start_date = start_date
        if end_date:
            phase.end_date = end_date
        phase.save()

    def get_embed_code(self, bplan):
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
        file_name = self._generate_image_filename(
            posixpath.basename(parsed_url.path))
        try:
            with request.urlopen(url) as f:
                file_name = self._image_storage.save(file_name, f)
        except Exception as e:
            self._image_storage.delete(file_name)
            raise serializers.ValidationError(
                'Failed to download image {}'.format(url))

        try:
            self._validate_image(file_name)
        except ValidationError as e:
            self._image_storage.delete(file_name)
            raise serializers.ValidationError(e)

        return file_name

    def _validate_image(self, file_name):
        image_file = self._image_storage.open(file_name, 'rb')
        image = ImageFile(image_file, file_name)
        config = settings.IMAGE_ALIASES.get('*', {})
        config.update(settings.IMAGE_ALIASES['tileimage'])
        validate_image(image, **config)

    @property
    def _image_storage(self):
        return project_models.Project._meta.get_field('tile_image').storage

    @property
    def _image_upload_to(self):
        return project_models.Project._meta.get_field('tile_image').upload_to

    def _generate_image_filename(self, filename):
        if callable(self._image_upload_to):
            raise Exception('Callable upload_to fields are not supported')

        dirname = datetime.datetime.now().strftime(self._image_upload_to)
        filename = posixpath.join(dirname, filename)
        return self._image_storage.get_available_name(filename)

    def _send_project_created_signal(self, bplan):
        a4dashboard_signals.project_created.send(
            sender=self.__class__,
            project=bplan,
            user=self.context['request'].user
        )

    def _send_component_updated_signal(self, bplan):
        component = components.projects['bplan']
        a4dashboard_signals.project_component_updated.send(
            sender=self.__class__,
            project=bplan,
            component=component,
            user=self.context['request'].user
        )
