from django import forms
from django.forms.fields import SplitDateTimeField
from django.utils.translation import gettext_lazy as _

from .widgets import DateTimeInput


class DateTimeField(SplitDateTimeField):
    widget = DateTimeInput

    def __init__(
        self, date_format=None, time_format=None, time_default=None, *args, **kwargs
    ):
        label = kwargs.get("label", None)
        time_label = ""
        if isinstance(label, tuple):
            date_label, time_label = label
            kwargs["label"] = date_label
        elif label:
            time_label = _("Time of %(date_label)s" % {"date_label": label})

        if "widget" not in kwargs:
            kwargs["widget"] = self.widget(
                date_format=date_format,
                time_format=time_format,
                time_label=time_label,
                time_default=time_default,
            )

        super().__init__(*args, **kwargs)

    def clean(self, value):
        value = self._set_default_time(value)
        return super().clean(value)

    def bound_data(self, data, initial):
        # If both fields are empty, set the data to None
        # This allows to mark required for publish fields
        if data == ["", ""]:
            return None

        data = self._set_default_time(data)
        return super().bound_data(data, initial)

    def _set_default_time(self, value):
        # Set the default time if only a date is submitted
        if isinstance(value, (list, tuple)):
            date, time = value
            if (
                not self.require_all_fields
                and time in self.empty_values
                and date not in self.empty_values
            ):
                value[1] = self.widget.get_default_time()
        return value

class CreatorContactFieldMixin(forms.ModelForm):
    creator_email = forms.EmailField(
        required=False,
        label=_("Your email address"),
        help_text=_("We will use this to contact you about your submission"),
    )
    creator_phone = forms.CharField(
        required=False,
        label=_("Phone number (optional)"),
        help_text=_("Optional contact number for follow-up questions"),
    )
    creator_contact_consent = forms.BooleanField(
        required=False,
        label=_("Contact consent"),
        help_text=_(
            "I expressly consent to the storage of the contact information I have provided. This information may only be used by the responsible authority to get in touch with me in connection with this project. I can withdraw this consent at any time. I have read and accept the Privacy Policy."
        ),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get("user", None)
        super().__init__(*args, **kwargs)

        # Set default creator_email to user's email
        if self.user and self.user.email:
            self.fields["creator_email"].initial = self.user.email

        self.fields["creator_email"].widget.attrs.update({"placeholder": _("Optional")})
        self.fields["creator_phone"].widget.attrs.update({"placeholder": _("Optional")})

    def clean_creator_email(self):
        """Ensure creator_email is either blank or a valid email."""
        email = self.cleaned_data.get("creator_email", "")
        return email if email else ""

    def save(self, commit=True):
        instance = super().save(commit=commit)
        
        if commit and hasattr(instance, "save"):
            posted_fields = set(self.data.keys()) if hasattr(self, 'data') else set()
            
            # Only update contact fields if they were actually in the form submission
            if 'creator_contact_consent' in posted_fields:
                consent = self.cleaned_data.get("creator_contact_consent", False)
                
                if not consent:
                    # Consent unchecked - clear email and phone
                    instance.creator_email = ""
                    instance.creator_phone = ""
                else:
                    # Consent checked - update only if submitted
                    if 'creator_email' in posted_fields:
                        instance.creator_email = self.cleaned_data.get("creator_email", "")
                    if 'creator_phone' in posted_fields:
                        instance.creator_phone = self.cleaned_data.get("creator_phone", "")
                
                instance.creator_contact_consent = consent
            
            instance.save()
        
        return instance