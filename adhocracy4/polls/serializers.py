import base64
import uuid

from django.conf import settings
from django.core.files.base import ContentFile
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from adhocracy4.projects.enums import Access
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
            validated_data["image_alt_text"] = ""
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
        from .validators import validate_poll_question_image

        validate_poll_question_image(value)
        return value


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, source="annotated_questions")
    has_user_vote = serializers.SerializerMethodField()
    guest_can_vote = serializers.SerializerMethodField()
    voting_ended = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = (
            "id",
            "questions",
            "has_user_vote",
            "allow_unregistered_users",
            "guest_can_vote",
            "voting_ended",
        )

    def get_has_user_vote(self, poll):
        user = self.context.get("request", {}).user
        if user and user.is_authenticated:
            return (
                Vote.objects.filter(choice__question__poll=poll, creator=user).exists()
                or Answer.objects.filter(question__poll=poll, creator=user).exists()
            )
        return False

    def get_guest_can_vote(self, poll):
        module = poll.module
        return (
            module.project.access == Access.PUBLIC
            and not module.project.is_draft
            and poll.allow_unregistered_users
            and module.active_phase is not None
            and module.active_phase.has_feature("crud", Vote)
        )

    def get_voting_ended(self, poll):
        return poll.module.phase_set.filter(end_date__lt=timezone.now()).exists()

    def update(self, instance, validated_data):
        from .services import PollUpdateService

        request = self.context.get("request")
        if not request:
            return instance

        service = PollUpdateService(instance, request)
        service.update_allow_unregistered(validated_data)

        questions_data = service.parse_questions()
        if not questions_data:
            return instance

        if getattr(settings, "A4_POLL_QUESTION_IMAGES", True):
            service.validate_question_images(questions_data)

        service.delete_removed_questions(questions_data)
        service.save_questions(questions_data)
        service.send_component_updated_signal()

        return instance
