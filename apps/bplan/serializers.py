from django.apps import apps
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from rest_framework import serializers

from .models import Bplan


BPLAN_EMBED = '<iframe height="500" style="width: 100%; min-height: 300px; ' \
              'max-height: 100vh" src="{}" frameborder="0"></iframe>'


class BplanSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    typ = serializers.HiddenField(default='Bplan')
    is_draft = serializers.HiddenField(default=False)

    class Meta:
        model = Bplan
        fields = (
            'id', 'name', 'description', 'is_archived', 'url',
            'office_worker_email', 'typ', 'is_draft'
        )

    def create(self, validated_data):
        orga_pk = self._context.get('organisation_pk', None)
        orga_model = apps.get_model(settings.A4_ORGANISATIONS_MODEL)
        orga = orga_model.objects.get(pk=orga_pk)
        validated_data['organisation'] = orga
        return super().create(validated_data)

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
