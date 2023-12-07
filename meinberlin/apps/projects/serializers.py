from functools import lru_cache

from django.utils import timezone
from django.utils.translation import gettext as _
from easy_thumbnails.files import get_thumbnailer
from rest_framework import fields
from rest_framework import serializers

from adhocracy4.phases.models import Phase
from adhocracy4.projects.models import Project
from adhocracy4.projects.models import Topic
from meinberlin.apps.plans.models import Plan


class CommonFields:
    @staticmethod
    def get_district(instance):
        city_wide = _("City wide")
        district_name = str(city_wide)
        if instance.administrative_district:
            district_name = instance.administrative_district.name
        return district_name

    @staticmethod
    def get_point(instance):
        point = instance.point
        if not point:
            point = ""
        return point

    @staticmethod
    def get_organisation(instance):
        return instance.organisation.name

    @staticmethod
    def get_created_or_modified(instance):
        if instance.modified:
            return fields.DateTimeField().to_representation(instance.modified)
        return fields.DateTimeField().to_representation(instance.created)


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ["code", "name"]


class ProjectSerializer(serializers.ModelSerializer, CommonFields):
    active_phase = serializers.SerializerMethodField()
    cost = serializers.SerializerMethodField()
    created_or_modified = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()
    future_phase = serializers.SerializerMethodField()
    organisation = serializers.SerializerMethodField()
    participation = serializers.SerializerMethodField()
    participation_active = serializers.SerializerMethodField()
    participation_string = serializers.SerializerMethodField()
    past_phase = serializers.SerializerMethodField()
    plan_title = serializers.SerializerMethodField()
    plan_url = serializers.SerializerMethodField()
    point = serializers.SerializerMethodField()
    point_label = serializers.SerializerMethodField()
    published_projects_count = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    subtype = serializers.SerializerMethodField()
    tile_image = serializers.SerializerMethodField()
    tile_image_alt_text = serializers.SerializerMethodField()
    tile_image_copyright = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    topics = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        self.now = kwargs.pop("now")
        super().__init__(args, kwargs)

    class Meta:
        model = Project
        fields = [
            "access",
            "active_phase",
            "cost",
            "created_or_modified",
            "description",
            "district",
            "future_phase",
            "organisation",
            "participation",
            "participation_active",
            "participation_string",
            "past_phase",
            "plan_title",
            "plan_url",
            "point",
            "point_label",
            "published_projects_count",
            "status",
            "subtype",
            "tile_image",
            "tile_image_alt_text",
            "tile_image_copyright",
            "title",
            "topics",
            "type",
            "url",
        ]

    def get_topics(self, instance):
        return [topic.code for topic in instance.topics.all()]

    @lru_cache(maxsize=1)
    def _get_participation_status_project(self, instance):
        project_phases = instance.phases

        if project_phases.active_phases():
            return _("running"), True

        if project_phases.future_phases():
            try:
                return (
                    _("starts at {}").format(
                        project_phases.future_phases()
                        .first()
                        .start_date.strftime("%d.%m.%Y")
                    ),
                    True,
                )
            except AttributeError:
                return (_("starts in the future"), True)
        else:
            return _("done"), False

    def get_type(self, instance):
        return "project"

    def get_subtype(self, instance):
        if instance.project_type in (
            "meinberlin_extprojects.ExternalProject",
            "meinberlin_bplan.Bplan",
        ):
            return "external"
        return "default"

    def get_title(self, instance):
        return instance.name

    def get_url(self, instance):
        if instance.project_type in (
            "meinberlin_extprojects.ExternalProject",
            "meinberlin_bplan.Bplan",
        ):
            return instance.externalproject.url
        return instance.get_absolute_url()

    def get_tile_image(self, instance):
        image_url = ""
        if instance.tile_image:
            image = get_thumbnailer(instance.tile_image)["project_tile"]
            image_url = image.url
        elif instance.image:
            image = get_thumbnailer(instance.image)["project_tile"]
            image_url = image.url
        return image_url

    def get_tile_image_alt_text(self, instance):
        if instance.tile_image:
            return instance.tile_image_alt_text
        elif instance.image:
            return instance.image_alt_text
        else:
            return None

    def get_tile_image_copyright(self, instance):
        if instance.tile_image:
            return instance.tile_image_copyright
        elif instance.image:
            return instance.image_copyright
        else:
            return None

    def get_status(self, instance):
        project_phases = instance.phases
        if project_phases.active_phases() or project_phases.future_phases():
            return 0
        return 1

    def get_participation(self, instance):
        return Plan.PARTICIPATION_CONSULTATION

    def get_future_phase(self, instance):
        if instance.future_modules and instance.future_modules.first().module_start:
            return fields.DateTimeField().to_representation(
                instance.future_modules.first().module_start
            )
        return False

    def get_active_phase(self, instance):
        if instance.active_phase_ends_next:
            progress = instance.module_running_progress
            time_left = instance.module_running_time_left
            end_date = fields.DateTimeField().to_representation(
                instance.running_module_ends_next.module_end
            )
            return [progress, time_left, end_date]
        return False

    def get_past_phase(self, instance):
        if instance.past_modules and instance.past_modules.first().module_end:
            return fields.DateTimeField().to_representation(
                instance.past_modules.first().module_end
            )
        return False

    def get_participation_string(self, instance):
        (
            participation_string,
            participation_active,
        ) = self._get_participation_status_project(instance)
        return str(participation_string)

    def get_participation_active(self, instance):
        (
            participation_string,
            participation_active,
        ) = self._get_participation_status_project(instance)
        return participation_active

    def get_plan_url(self, instance):
        if instance.plans.exists():
            return instance.plans.first().get_absolute_url()
        return None

    def get_plan_title(self, instance):
        if instance.plans.exists():
            return instance.plans.first().title
        return None

    def get_published_projects_count(self, instance):
        return 0

    def get_point_label(self, instance):
        return ""

    def get_cost(self, instance):
        return ""


class ActiveProjectSerializer(ProjectSerializer):
    def seconds_in_units(self, seconds):
        unit_totals = []

        unit_limits = [
            ([_("day"), _("days")], 24 * 3600),
            ([_("hour"), _("hours")], 3600),
            ([_("minute"), _("minutes")], 60),
            ([_("second"), _("seconds")], 1),
        ]

        for unit_name, limit in unit_limits:
            if seconds >= limit:
                amount = int(float(seconds) / limit)
                if amount > 1:
                    unit_totals.append((unit_name[1], amount))
                else:
                    unit_totals.append((unit_name[0], amount))
                seconds = seconds - (amount * limit)
        return unit_totals

    def get_active_phase(self, instance):
        progress = instance.module_running_progress
        time_left = instance.module_running_time_left
        end_date = fields.DateTimeField().to_representation(
            instance.running_module_ends_next.module_end
        )
        return [progress, time_left, end_date]

    def get_status(self, instance):
        return 0

    def get_future_phase(self, instance):
        return False

    def get_past_phase(self, instance):
        return False

    def get_participation_string(self, instance):
        return _("running")

    def get_participation_active(self, instance):
        return True


class FutureProjectSerializer(ProjectSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._future_phases = Phase.objects.filter(
            start_date__gt=self.now, module__is_draft=False
        ).order_by("start_date")

    def get_active_phase(self, instance):
        return False

    def get_status(self, instance):
        return 0

    def get_future_phase(self, instance):
        future_phase = self._future_phases.filter(module__project=instance).first()
        return fields.DateTimeField().to_representation(future_phase.start_date)

    def get_past_phase(self, instance):
        return False

    def get_participation_string(self, instance):
        return _("starts in the future")

    def get_participation_active(self, instance):
        return True


class PastProjectSerializer(ProjectSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._past_phases = Phase.objects.filter(
            end_date__lt=timezone.now(), module__is_draft=False
        ).order_by("start_date")

    def get_active_phase(self, instance):
        return False

    def get_status(self, instance):
        return 1

    def get_future_phase(self, instance):
        return False

    def get_past_phase(self, instance):
        past_phase = self._past_phases.filter(module__project=instance).first()
        return fields.DateTimeField().to_representation(past_phase.end_date)

    def get_participation_string(self, instance):
        return _("done")

    def get_participation_active(self, instance):
        return False
