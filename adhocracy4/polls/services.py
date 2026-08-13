import base64
import json
import re

from django.conf import settings
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.files.base import ContentFile
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from adhocracy4.dashboard import components
from adhocracy4.dashboard import signals as a4dashboard_signals

from .models import Choice
from .models import Question
from .validators import validate_poll_question_image


class PollUpdateService:
    """Encapsulates the logic for bulk-updating a poll's questions and choices
    from dashboard form submissions."""

    def __init__(self, poll, request):
        self.poll = poll
        self.request = request

    def update_allow_unregistered(self, validated_data):
        self.poll.allow_unregistered_users = (
            validated_data.get("allow_unregistered_users", False)
            if getattr(settings, "A4_POLL_ENABLE_UNREGISTERED_USERS", False)
            else False
        )
        self.poll.save()

    def update_hide_results(self, validated_data):
        self.poll.hide_results_until_finished = validated_data.get(
            "hide_results_until_finished", self.poll.hide_results_until_finished
        )
        self.poll.save()

    def parse_questions(self):
        if not hasattr(self.request, "data") or not self.request.data:
            return []

        data = self.request.data
        if "questions" in data:
            questions = data.get("questions", [])
            return json.loads(questions) if isinstance(questions, str) else questions

        if isinstance(data, dict):
            questions_dict = {}
            for key, value in data.items():
                match = re.match(r"questions\[(\d+)\]\.(.+)", key) or re.match(
                    r"questions\[(\d+)\]\[(.+)\]", key
                )
                if match:
                    idx, field = int(match.group(1)), match.group(2)
                    questions_dict.setdefault(idx, {})

                    if field.startswith("choices"):
                        choice_match = re.search(r"choices\[(\d+)\]\.(.+)", field)
                        if choice_match:
                            c_idx, c_field = (
                                int(choice_match.group(1)),
                                choice_match.group(2),
                            )
                            questions_dict[idx].setdefault("choices", []).append({})
                            while len(questions_dict[idx]["choices"]) <= c_idx:
                                questions_dict[idx]["choices"].append({})
                            try:
                                questions_dict[idx]["choices"][c_idx][c_field] = (
                                    json.loads(value)
                                )
                            except (json.JSONDecodeError, TypeError):
                                questions_dict[idx]["choices"][c_idx][c_field] = value
                    else:
                        try:
                            questions_dict[idx][field] = json.loads(value)
                        except (json.JSONDecodeError, TypeError):
                            questions_dict[idx][field] = value

            return [questions_dict[i] for i in sorted(questions_dict.keys())]

        return []

    def validate_question_images(self, questions_data):
        question_errors = []
        has_errors = False

        for q_data in questions_data:
            q_error = {}

            image_data = q_data.get("image") or q_data.get("image_base64")
            try:
                validate_poll_question_image(image_data)
            except serializers.ValidationError as e:
                detail = e.detail.get("image_base64", [])
                if isinstance(detail, str):
                    detail = [detail]
                q_error["image_base64"] = detail

            if not q_error.get("image_base64"):
                image_alt_text = q_data.get("image_alt_text", "")
                if not image_alt_text:
                    has_image = bool(image_data and image_data != "")
                    if not has_image and image_data != "":
                        q_id = q_data.get("id")
                        if q_id:
                            try:
                                existing = Question.objects.get(id=q_id)
                                has_image = bool(existing.image)
                            except Question.DoesNotExist:
                                pass
                    if has_image:
                        q_error["image_alt_text"] = [
                            _(
                                "Please provide a descriptive alt text for "
                                "the question image."
                            )
                        ]

            question_errors.append(q_error)
            if q_error:
                has_errors = True

        if has_errors:
            raise serializers.ValidationError({"questions": question_errors})

    def delete_removed_questions(self, questions_data):
        keep_ids = {q["id"] for q in questions_data if q.get("id")}
        for q_id in set(self.poll.questions.values_list("id", flat=True)) - keep_ids:
            self._delete_question_with_image(q_id)

    def save_questions(self, questions_data):
        question_images_enabled = getattr(settings, "A4_POLL_QUESTION_IMAGES", True)

        for weight, q_data in enumerate(questions_data):
            defaults = {
                "poll": self.poll,
                "label": q_data.get("label", ""),
                "help_text": q_data.get("help_text", ""),
                "multiple_choice": q_data.get("multiple_choice", False),
                "is_open": q_data.get("is_open", False),
                "is_confidential": q_data.get("is_confidential", False),
                "weight": weight,
            }
            if question_images_enabled:
                defaults["image_alt_text"] = q_data.get("image_alt_text", "")

            question, created = Question.objects.update_or_create(
                id=q_data.get("id"),
                defaults=defaults,
            )

            if question_images_enabled:
                image_data = q_data.get("image") or q_data.get("image_base64")
                try:
                    self._handle_question_image(question, image_data)
                except serializers.ValidationError as e:
                    nested = [{} for _ in questions_data]
                    nested[weight] = e.detail
                    raise serializers.ValidationError({"questions": nested})
            if not question.is_open and "choices" in q_data:
                self._update_choices(q_data["choices"], question)

    def send_component_updated_signal(self):
        component = components.modules["polls"]
        a4dashboard_signals.module_component_updated.send(
            sender=component.__class__,
            module=self.poll.module,
            component=component.__class__,
            user=self.request.user,
        )

    def _delete_question_with_image(self, q_id):
        question = Question.objects.filter(id=q_id, poll=self.poll).first()
        if question:
            if question.image:
                question.image.delete(save=False)
            question.delete()

    def _handle_question_image(self, question_instance, image_data):
        if image_data == "":
            if question_instance.image:
                question_instance.image.delete(save=False)
            question_instance.image = None
            question_instance.image_alt_text = ""
            question_instance.save()
        elif image_data and "base64," in image_data:
            format, imgstr = image_data.split(";base64,")
            ext = format.split("/")[-1]
            if question_instance.image:
                question_instance.image.delete(save=False)
            try:
                question_instance.image.save(
                    f"question_{question_instance.id}.{ext}",
                    ContentFile(base64.b64decode(imgstr)),
                    save=True,
                )
            except DjangoValidationError as e:
                raise serializers.ValidationError({"image_base64": e.messages})

    def _update_choices(self, choices_data, question_instance):
        existing_ids = set(question_instance.choices.values_list("id", flat=True))
        keep_ids = {c["id"] for c in choices_data if c.get("id")}

        Choice.objects.filter(
            id__in=existing_ids - keep_ids, question=question_instance
        ).delete()

        for weight, choice_data in enumerate(choices_data):
            Choice.objects.update_or_create(
                id=choice_data.get("id"),
                defaults={
                    "question": question_instance,
                    "label": choice_data.get("label", ""),
                    "is_other_choice": choice_data.get("is_other_choice", False),
                    "weight": weight,
                },
            )
