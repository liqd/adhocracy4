import datetime
import imghdr
import posixpath
import tempfile
from urllib.parse import urlparse

import requests
from django.apps import apps
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.files.images import ImageFile
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from pyproj import Transformer
from rest_framework import serializers

from adhocracy4.dashboard import components
from adhocracy4.dashboard import signals as a4dashboard_signals
from adhocracy4.images.validators import validate_image
from adhocracy4.modules import models as module_models
from adhocracy4.phases import models as phase_models
from adhocracy4.projects import models as project_models

from .models import Bplan
from .phases import StatementPhase

BPLAN_EMBED = (
    '<iframe height="500" style="width: 100%; min-height: 300px; '
    'max-height: 100vh" src="{}" frameborder="0"></iframe>'
)
DOWNLOAD_IMAGE_SIZE_LIMIT_BYTES = 10 * 1024 * 1024


class BplanSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    # make write_only for consistency  reasons
    start_date = serializers.DateTimeField(write_only=True)
    end_date = serializers.DateTimeField(write_only=True)
    image_url = serializers.URLField(
        required=False,
        write_only=True,
    )
    # can't use a4 field as must be serilizer field
    image_alt_text = serializers.CharField(
        required=False,
        write_only=True,
        allow_blank=True,
        source="tile_image_alt_text",
        max_length=(
            project_models.Project._meta.get_field("tile_image_alt_text").max_length
        ),
    )
    image_copyright = serializers.CharField(
        required=False,
        write_only=True,
        source="tile_image_copyright",
        allow_blank=True,
        max_length=(
            project_models.Project._meta.get_field("tile_image_copyright").max_length
        ),
    )
    embed_code = serializers.SerializerMethodField()
    # # overwrite the point model field so it's expecting json, the original field is validated as a string and therefore
    # # doesn't pass validation when not receiving a string
    # point = serializers.JSONField(required=False, write_only=True)
    bplan_id = serializers.CharField(
        required=False,
        write_only=True,
    )

    class Meta:
        model = Bplan
        fields = (
            "id",
            "name",
            "identifier",
            "bplan_id",
            "description",
            "url",
            "office_worker_email",
            "is_diplan",
            "is_draft",
            "start_date",
            "end_date",
            "image_url",
            "image_alt_text",
            "image_copyright",
            "embed_code",
            "point",
        )
        extra_kwargs = {
            # write_only for consistency reasons
            "is_draft": {"default": False, "write_only": True},
            "is_diplan": {"default": False, "write_only": True},
            "name": {"write_only": True},
            "description": {"write_only": True},
            "url": {"write_only": True},
            "office_worker_email": {"write_only": True},
            "identifier": {"write_only": True},
            "point": {"write_only": True, "required": False},
        }

    def to_representation(self, instance):
        """Removes the `embed_code` if the bplan is coming from diplan.
        Bit hacky but this can be removed once the transition to diplan is completed,"""
        ret = super().to_representation(instance)
        if instance.is_diplan:
            ret.pop("embed_code")
        return ret

    def create(self, validated_data):
        orga_pk = self._context.get("organisation_pk", None)
        orga_model = apps.get_model(settings.A4_ORGANISATIONS_MODEL)
        orga = orga_model.objects.get(pk=orga_pk)
        validated_data["organisation"] = orga

        # mark as diplan, will make removal of old bplans easier
        # TODO: remove this check and the is_diplan field once transition to diplan is completed
        if "bplan_id" in validated_data or "point" in validated_data:
            validated_data["is_diplan"] = True

        # TODO: rename identifier to bplan_id on model and remove the custom logic here
        if "bplan_id" in validated_data:
            bplan_id = validated_data.pop("bplan_id")
            validated_data["identifier"] = bplan_id

        # We receive the point as a string containing coordinates in epsg3875 but internally
        # use epsg4326 so we need to convert them and save them as valid geojson
        if "point" in validated_data:
            point = validated_data["point"].split(",")
            transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326")
            new_point = transformer.transform(point[0].strip(), point[1].strip())
            validated_data["point"] = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [new_point[1], new_point[0]],
                },
            }

        start_date = validated_data["start_date"]
        end_date = validated_data["end_date"]

        image_url = validated_data.pop("image_url", None)
        if image_url:
            validated_data["tile_image"] = self._download_image_from_url(image_url)

        bplan = super().create(validated_data)

        self._create_module_and_phase(bplan, start_date, end_date)
        self._send_project_created_signal(bplan)
        return bplan

    def _create_module_and_phase(self, bplan, start_date, end_date):
        module = module_models.Module.objects.create(
            name=bplan.slug + "_module",
            weight=1,
            project=bplan,
        )

        phase_content = StatementPhase()
        phase_models.Phase.objects.create(
            name=_("Bplan statement phase"),
            description=_("Bplan statement phase"),
            type=phase_content.identifier,
            module=module,
            start_date=start_date,
            end_date=end_date,
        )

    def update(self, instance, validated_data):
        start_date = validated_data.get("start_date", None)
        end_date = validated_data.get("end_date", None)
        if start_date or end_date:
            self._update_phase(instance, start_date, end_date)
            # TODO: remove as we don't need to archive bplans anymore once the transition to diplan is complete as
            #  they unpublish them if they should no longer be shown
            if end_date and end_date > timezone.localtime(timezone.now()):
                instance.is_archived = False

        # mark as diplan, will make removal of old bplans easier
        # TODO: remove this check and the is_diplan field once transition to diplan is completed
        if "bplan_id" in validated_data or "point" in validated_data:
            validated_data["is_diplan"] = True

        # TODO: rename identifier to bplan_id on model and remove the custom logic here
        if "bplan_id" in validated_data:
            bplan_id = validated_data.pop("bplan_id")
            validated_data["identifier"] = bplan_id

        # We receive the point as a string containing coordinates in epsg3875 but internally
        # use epsg4326 so we need to convert them and save them as valid geojson
        if "point" in validated_data:
            point = validated_data["point"].split(",")
            transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326")
            new_point = transformer.transform(point[0].strip(), point[1].strip())
            validated_data["point"] = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [new_point[1], new_point[0]],
                },
            }

        image_url = validated_data.pop("image_url", None)
        if image_url:
            validated_data["tile_image"] = self._download_image_from_url(image_url)

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
        if bplan.is_diplan:
            return None
        url = self._get_absolute_url(bplan)
        embed = BPLAN_EMBED.format(url)
        return embed

    def _get_absolute_url(self, bplan):
        site_url = Site.objects.get_current().domain
        embed_url = reverse(
            "embed-project",
            kwargs={
                "slug": bplan.slug,
            },
        )
        url = "https://{}{}".format(site_url, embed_url)
        return url

    def _download_image_from_url(self, url):
        parsed_url = urlparse(url)
        file_name = None
        try:
            r = requests.get(url, stream=True, timeout=10)
            downloaded_bytes = 0
            with tempfile.TemporaryFile() as f:
                for chunk in r.iter_content(chunk_size=1024):
                    downloaded_bytes += len(chunk)
                    if downloaded_bytes > DOWNLOAD_IMAGE_SIZE_LIMIT_BYTES:
                        raise serializers.ValidationError(
                            "Image too large to download {}".format(url)
                        )
                    if chunk:
                        f.write(chunk)
                file_name = self._generate_image_filename(parsed_url.path, f)
                self._image_storage.save(file_name, f)
        except Exception:
            if file_name:
                self._image_storage.delete(file_name)
            raise serializers.ValidationError("Failed to download image {}".format(url))

        try:
            self._validate_image(file_name)
        except ValidationError as e:
            self._image_storage.delete(file_name)
            raise serializers.ValidationError(e)

        return file_name

    def _validate_image(self, file_name):
        image_file = self._image_storage.open(file_name, "rb")
        image = ImageFile(image_file, file_name)
        config = settings.IMAGE_ALIASES.get("*", {})
        config.update(settings.IMAGE_ALIASES["tileimage"])
        validate_image(image, **config)

    @property
    def _image_storage(self):
        return project_models.Project._meta.get_field("tile_image").storage

    @property
    def _image_upload_to(self):
        return project_models.Project._meta.get_field("tile_image").upload_to

    def _generate_image_filename(self, url_path, file):
        if callable(self._image_upload_to):
            raise Exception("Callable upload_to fields are not supported")

        root_path, extension = posixpath.splitext(url_path)
        if file:
            # Workaround: imghdr expects the files position on 0
            file.seek(0)
            extension = imghdr.what(file) or "jpeg"

        basename = "bplan_%s" % (timezone.now().strftime("%Y%m%dT%H%M%S"))

        dirname = datetime.datetime.now().strftime(self._image_upload_to)
        filename = posixpath.join(dirname, basename + "." + extension)

        return self._image_storage.get_available_name(filename)

    def _send_project_created_signal(self, bplan):
        a4dashboard_signals.project_created.send(
            sender=self.__class__, project=bplan, user=self.context["request"].user
        )

    def _send_component_updated_signal(self, bplan):
        component = components.projects["bplan"]
        a4dashboard_signals.project_component_updated.send(
            sender=self.__class__,
            project=bplan,
            component=component,
            user=self.context["request"].user,
        )
