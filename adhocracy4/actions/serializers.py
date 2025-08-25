from django.template.defaultfilters import truncatechars
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.timezone import localtime
from rest_framework import serializers

from adhocracy4.actions.models import Action
from adhocracy4.projects.serializers import ProjectSerializer


class ActionSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    source = serializers.SerializerMethodField()
    source_timestamp = serializers.SerializerMethodField()
    body = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()
    item = serializers.SerializerMethodField()
    actor = serializers.SerializerMethodField()
    target_creator = serializers.CharField(
        source="target_creator.username", default=None
    )
    project = ProjectSerializer(source="project", now=timezone.now())

    _cache = {}

    class Meta:
        model = Action
        exclude = (
            "obj_content_type",
            "obj_comment_creator",
            "description",
            "verb",
            "target_object_id",
            "obj_object_id",
            "public",
            "target_content_type",
        )

    def get_cached_trigger(self, obj):
        trigger = self._cache.setdefault(
            f"trigger-${obj.id}",
            obj.obj_content_type.get_object_for_this_type(pk=obj.obj_object_id),
        )

        return (trigger, trigger.__class__.__name__)

    def get_cached_target(self, obj):
        if not obj.target_content_type:
            return None

        target = self._cache.setdefault(
            f"target-${obj.id}",
            obj.target_content_type.get_object_for_this_type(pk=obj.target_object_id),
        )

        return target

    def get_body(self, obj):
        trigger, trigger_class = self.get_cached_trigger(obj)
        target = self.get_cached_target(obj)
        body = None

        if trigger_class == "ModeratorRemark":
            body = strip_tags(target.moderator_feedback_text.feedback_text)
        elif trigger_class == "Comment":
            body = trigger.notification_content
        elif trigger_class == "Rating":
            possible_attributes = ["notification_content", "name"]
            for attr in possible_attributes:
                if hasattr(target, attr):
                    body = getattr(target, attr)
                    break

        return truncatechars(body, 50) if body else None

    def get_link(self, obj):
        trigger, trigger_class = self.get_cached_trigger(obj)

        if trigger_class == "ModeratorRemark":
            return trigger.item.get_absolute_url()
        if trigger_class == "Rating":
            return trigger.content_object.get_absolute_url()
        if trigger_class == "Phase":
            return trigger.module.get_absolute_url()
        if hasattr(trigger, "get_absolute_url"):
            return trigger.get_absolute_url()
        return None

    def get_item(self, obj):
        if obj.type == "item":
            return None
        target = self.get_cached_target(obj)

        if target and hasattr(target, "name"):
            return target.name
        elif target and hasattr(target, "content_object"):
            if hasattr(target.content_object, "name"):
                return target.content_object.name
            elif hasattr(target.content_object, "module"):
                return target.content_object.module.name
        return None

    def get_type(self, obj):
        trigger = self.get_cached_target(obj)
        if obj.type == "rating" and trigger.__class__.__name__ == "Proposal":
            return "support"
        if obj.type == "phase" and obj.verb == "schedule":
            return "phase_soon_over"
        if obj.type == "phase" and obj.verb == "start":
            return "phase_started"
        if obj.type == "project" and obj.verb == "publish":
            return "project_published"
        return obj.type

    def get_source(self, obj):
        trigger, _ = self.get_cached_trigger(obj)

        if trigger and hasattr(trigger, "name"):
            return trigger.name
        elif trigger and hasattr(trigger, "content_object"):
            return trigger.content_object.__class__.__name__.lower()

    def get_source_timestamp(self, obj):
        trigger, _ = self.get_cached_trigger(obj)

        if trigger and hasattr(trigger, "date"):
            return localtime(trigger.date)
        return None

    def is_moderator(self, obj):
        return obj.actor in obj.project.moderators.all()

    def get_actor(self, obj):
        if not obj.actor:
            return {"username": "system", "is_moderator": False}

        return {
            "username": obj.actor.username,
            "is_moderator": self.is_moderator(obj),
        }
