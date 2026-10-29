from html import unescape

from django import forms
from django.utils.html import linebreaks
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _


class ModerationItemFeedbackForm(forms.Form):
    """Edit the moderation status and official feedback of an item.

    The form only contains the fields the item actually provides.
    """

    moderator_status = forms.ChoiceField(
        required=False,
        label=_("Status (public)"),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    feedback_text = forms.CharField(
        required=False,
        label=_("Feedback (public)"),
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "class": "a4-comments__textarea--small form-group",
            }
        ),
    )

    def __init__(self, *args, item, **kwargs):
        self.item = item
        self.changed = False
        super().__init__(*args, **kwargs)

        if not self._has_field("moderator_status"):
            del self.fields["moderator_status"]
            self._initial_status = ""
        else:
            status_field = self.item._meta.get_field("moderator_status")
            if status_field.choices:
                choices = [("", _("No status"))]
                choices.extend(status_field.choices)
                self.fields["moderator_status"].choices = choices
            else:
                self.fields["moderator_status"] = forms.CharField(
                    required=False,
                    label=_("Status (public)"),
                    max_length=getattr(status_field, "max_length", None),
                    widget=forms.TextInput(attrs={"class": "form-select"}),
                )
            self._initial_status = self.item.moderator_status or ""
            self.initial["moderator_status"] = self._initial_status

        if not self._has_field("moderator_feedback_text"):
            del self.fields["feedback_text"]
            self._initial_feedback_text = ""
        else:
            self._initial_feedback_text = self._feedback_text()
            self.initial["feedback_text"] = self._initial_feedback_text

    def _has_field(self, name):
        return any(field.name == name for field in self.item._meta.get_fields())

    def _feedback_model(self):
        return self.item._meta.get_field("moderator_feedback_text").related_model

    def _feedback_text(self):
        feedback = self.item.moderator_feedback_text
        if feedback is None:
            return ""
        return unescape(strip_tags(feedback.feedback_text or ""))

    def save(self, user):
        if "moderator_status" in self.fields:
            status_field = self.item._meta.get_field("moderator_status")
            status = self.cleaned_data["moderator_status"] or (
                None if status_field.null else ""
            )
            if (status or "") != self._initial_status:
                self.item.moderator_status = status
                self.changed = True

        if "feedback_text" in self.fields:
            text = self.cleaned_data["feedback_text"]
            if text != self._initial_feedback_text:
                feedback = self.item.moderator_feedback_text
                if feedback is None:
                    feedback = self._feedback_model()(creator=user)
                feedback.feedback_text = linebreaks(text) if text else ""
                feedback.save()
                self.item.moderator_feedback_text = feedback
                self.changed = True

        self.item.is_reviewed = True
        self.item.save()
        return self.item
