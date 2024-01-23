from django import forms
from django.utils.translation import gettext_lazy as _

from adhocracy4.forms.fields import DateTimeField

from . import models


class OfflineEventForm(forms.ModelForm):
    date = DateTimeField(
        time_format="%H:%M",
        required=True,
        require_all_fields=False,
        label=(_("Date"), _("Time")),
    )

    class Meta:
        model = models.OfflineEvent
        fields = ["name", "event_type", "date", "description"]
        help_texts = {
            "description": _(
                "If you add an image, please provide an alternate text. "
                "It serves as a textual description of the image content "
                "and is read out by screen readers. Describe the image "
                "in approx. 80 characters. Example: A busy square with "
                "people in summer."
            ),
            "event_type": _(
                "The content of this field is shown in the timeline. It "
                "should have no more than 30 characters e.g. Information "
                "event or 3rd public workshop."
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date"].label = _("Date and time")
