import base64
import json
import re
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.files.base import ContentFile
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from adhocracy4.dashboard import components
from adhocracy4.dashboard import signals as a4dashboard_signals
from adhocracy4.rules.discovery import NormalUser

from .models import Answer
from .models import Choice
from .models import OtherVote
from .models import Poll
from .models import Question
from .models import Vote


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ("id", "answer")


class OtherChoiceAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherVote
        fields = ("vote_id", "answer")


class ChoiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    count = serializers.SerializerMethodField()

    class Meta:
        model = Choice
        fields = ("id", "label", "count", "is_other_choice")

    def get_count(self, choice: Choice) -> int:
        if choice.question.is_confidential:
            return 0
        return getattr(choice, "vote_count", choice.votes.all().count())


class QuestionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not getattr(settings, "A4_POLL_QUESTION_IMAGES", True):
            for field in [
                "image_base64",
                "image_url",
                "image_alt_text",
                "image_help_text",
            ]:
                self.fields.pop(field, None)

    isReadOnly = serializers.SerializerMethodField(method_name="get_is_read_only")
    authenticated = serializers.SerializerMethodField()
    choices = ChoiceSerializer(many=True)
    userChoices = serializers.SerializerMethodField(method_name="get_user_choices")
    answers = serializers.SerializerMethodField(method_name="get_answers")
    userAnswer = serializers.SerializerMethodField(method_name="get_user_answer")
    other_choice_answers = serializers.SerializerMethodField(
        method_name="get_other_choice_answers"
    )
    other_choice_user_answer = serializers.SerializerMethodField(
        method_name="get_other_choice_user_answer"
    )
    totalVoteCount = serializers.SerializerMethodField(
        method_name="get_total_vote_count"
    )
    totalVoteCountMulti = serializers.SerializerMethodField(
        method_name="get_total_vote_count_multi"
    )
    totalAnswerCount = serializers.SerializerMethodField(
        method_name="get_total_answer_count"
    )
    image_base64 = serializers.CharField(
        required=False, allow_blank=True, allow_null=True, write_only=True
    )
    image_url = serializers.SerializerMethodField(method_name="get_image_url")
    image_help_text = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = (
            "id",
            "label",
            "help_text",
            "image_base64",
            "image_url",
            "image_alt_text",
            "image_help_text",
            "multiple_choice",
            "is_open",
            "is_confidential",
            "isReadOnly",
            "authenticated",
            "choices",
            "userChoices",
            "answers",
            "userAnswer",
            "other_choice_answers",
            "other_choice_user_answer",
            "totalVoteCount",
            "totalVoteCountMulti",
            "totalAnswerCount",
        )

    def get_image_url(self, question):
        return question.image.url if question.image else None

    def get_image_help_text(self, question):
        return str(question._meta.get_field("image").help_text)

    def _base64_to_image(self, base64_str):
        if "base64," in base64_str:
            format, imgstr = base64_str.split(";base64,")
            ext = format.split("/")[-1]
        else:
            imgstr, ext = base64_str, "png"

        return ContentFile(base64.b64decode(imgstr), name=f"{uuid.uuid4()}.{ext}")

    def _handle_image(self, validated_data):
        image_base64 = validated_data.pop("image_base64", None)
        if image_base64:
            return self._base64_to_image(image_base64)
        elif image_base64 == "":
            return None
        return None

    def create(self, validated_data):
        image = self._handle_image(validated_data)
        if image:
            validated_data["image"] = image
        return super().create(validated_data)

    def update(self, instance, validated_data):
        image = self._handle_image(validated_data)
        if image:
            validated_data["image"] = image
        elif image is None and "image_base64" in validated_data:
            validated_data["image"] = None
        return super().update(instance, validated_data)

    def get_authenticated(self, _):
        return (
            self.context.get("request", {}).user.is_authenticated
            if "request" in self.context
            else False
        )

    def get_is_read_only(self, question: Question):
        if "request" not in self.context:
            return True
        user = self.context["request"].user
        has_perm = user.has_perm("a4polls.add_vote", question.poll)
        would_have_perm = NormalUser().would_have_perm(
            "a4polls.add_vote", question.poll
        )
        return not has_perm and not would_have_perm

    def get_user_choices(self, question: Question):
        user = self.context.get("request", {}).user
        if user and user.is_authenticated:
            return question.user_choices_list(user)
        return []

    def _filter_own(self, queryset):
        user = self.context.get("request", {}).user
        if user and user.is_authenticated:
            return queryset.filter(creator=user)
        return queryset.none()

    def get_answers(self, question: Question):
        answers = question.answers.all()
        if question.is_confidential:
            answers = self._filter_own(answers)
        return AnswerSerializer(answers, many=True).data

    def get_user_answer(self, question: Question):
        user = self.context.get("request", {}).user
        if user and user.is_authenticated:
            return question.user_answer(user)
        return ""

    def get_other_choice_answers(self, question):
        answers = question.other_choice_answers()
        if question.is_confidential:
            user = self.context.get("request", {}).user
            if user and user.is_authenticated:
                answers = answers.filter(vote__creator=user)
            else:
                answers = answers.none()
        return OtherChoiceAnswerSerializer(answers, many=True).data

    def get_other_choice_user_answer(self, question: Question):
        user = self.context.get("request", {}).user
        if user and user.is_authenticated:
            return question.other_choice_user_answer(user)
        return ""

    def get_total_vote_count(self, question):
        return getattr(question, "vote_count", -1)

    def get_total_vote_count_multi(self, question):
        return getattr(question, "vote_count_multi", -1)

    def get_total_answer_count(self, question):
        return getattr(question, "answer_count", -1)

    def validate(self, data):
        image_base64 = data.get("image_base64")
        image_alt_text = data.get("image_alt_text", "")

        if image_base64 and not image_alt_text:
            raise serializers.ValidationError(
                {
                    "image_alt_text": [
                        _(
                            "Please provide a descriptive alt text for the question "
                            "image."
                        )
                    ]
                }
            )

        return data

    def validate_image_base64(self, value):
        """Validate image dimensions before processing"""
        if not value or value == "":
            return value

        if "base64," in value:
            import base64
            from io import BytesIO

            from PIL import Image

            format, imgstr = value.split(";base64,")
            image_data = base64.b64decode(imgstr)
            img = Image.open(BytesIO(image_data))

            if img.width < 1500:
                raise serializers.ValidationError(
                    "Image must be at least 1500 pixels wide"
                )
            if img.height < 500:
                raise serializers.ValidationError(
                    "Image must be at least 500 pixels high"
                )

        return value


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, source="annotated_questions")
    has_user_vote = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = ("id", "questions", "has_user_vote", "allow_unregistered_users")

    def get_has_user_vote(self, poll):
        user = self.context.get("request", {}).user
        if user and user.is_authenticated:
            return (
                Vote.objects.filter(choice__question__poll=poll, creator=user).exists()
                or Answer.objects.filter(question__poll=poll, creator=user).exists()
            )
        return False

    def _parse_questions_data(self, request):
        if not hasattr(request, "data") or not request.data:
            return []

        data = request.data
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
                            c_idx, c_field = int(
                                choice_match.group(1)
                            ), choice_match.group(2)
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

    def _delete_question_with_image(self, q_id, poll):
        question = Question.objects.filter(id=q_id, poll=poll).first()
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

    def update(self, instance, validated_data):
        instance.allow_unregistered_users = (
            validated_data.get("allow_unregistered_users", False)
            if getattr(settings, "A4_POLL_ENABLE_UNREGISTERED_USERS", False)
            else False
        )
        instance.save()

        request = self.context.get("request")
        if not request:
            return instance

        questions_data = self._parse_questions_data(request)
        if not questions_data:
            return instance

        question_images_enabled = getattr(settings, "A4_POLL_QUESTION_IMAGES", True)

        if question_images_enabled:
            from io import BytesIO

            from PIL import Image

            question_errors = []
            has_errors = False

            for q_data in questions_data:
                q_error = {}

                image_data = q_data.get("image") or q_data.get("image_base64")
                if image_data and image_data != "" and "base64," in image_data:
                    format, imgstr = image_data.split(";base64,")
                    image_bytes = base64.b64decode(imgstr)
                    img = Image.open(BytesIO(image_bytes))

                    if img.width < 1500:
                        q_error["image_base64"] = [
                            _("Image must be at least 1500 pixels wide")
                        ]
                    elif img.height < 500:
                        q_error["image_base64"] = [
                            _("Image must be at least 500 pixels high")
                        ]

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

        # Delete removed questions
        keep_ids = {q["id"] for q in questions_data if q.get("id")}
        for q_id in set(instance.questions.values_list("id", flat=True)) - keep_ids:
            self._delete_question_with_image(q_id, instance)

        # Update or create questions
        for weight, q_data in enumerate(questions_data):
            defaults = {
                "poll": instance,
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

        self._send_component_updated_signal(instance)
        return instance

    def _send_component_updated_signal(self, poll_instance):
        component = components.modules["polls"]
        a4dashboard_signals.module_component_updated.send(
            sender=component.__class__,
            module=poll_instance.module,
            component=component.__class__,
            user=self.context["request"].user,
        )
