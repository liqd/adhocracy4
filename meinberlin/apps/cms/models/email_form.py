from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail import fields
from wagtail.admin import panels
from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.models import AbstractEmailForm
from wagtail.contrib.forms.models import AbstractFormField

from meinberlin.apps.captcha.fields import CaptcheckCaptchaField
from meinberlin.apps.cms import emails


class EmailFormField(AbstractFormField):
    page = ParentalKey("EmailFormPage", related_name="form_fields")


class WagtailCaptchaFormBuilder(FormBuilder):
    @property
    def formfields(self):
        # Add captcha to formfields property
        fields = super().formfields
        if hasattr(settings, "CAPTCHA_URL") and settings.CAPTCHA_URL:
            fields["captcha"] = CaptcheckCaptchaField(label=_("I am not a robot"))

        return fields


class WagtailCaptchaEmailForm(AbstractEmailForm):
    """For pages implementing AbstractEmailForms with captcha."""

    form_builder = WagtailCaptchaFormBuilder

    def process_form_submission(self, form):
        form.fields.pop("captcha", None)
        form.cleaned_data.pop("captcha", None)
        return super().process_form_submission(form)

    class Meta:
        abstract = True


class EmailFormPage(WagtailCaptchaEmailForm):
    intro = fields.RichTextField(help_text="Introduction text shown above the form")
    thank_you = fields.RichTextField(
        help_text="Text shown after form submission",
    )
    email_content = models.CharField(
        max_length=200,
        help_text="Email content message",
    )
    attach_as = models.CharField(
        max_length=3,
        choices=(
            ("inc", "Include in Email"),
            ("xls", "XLSX Document"),
            ("txt", "Text File"),
        ),
        default="inc",
        help_text="Form results are send in this document format",
    )

    content_panels = AbstractEmailForm.content_panels + [
        panels.MultiFieldPanel(
            [
                panels.FieldPanel("intro", classname="full"),
                panels.FieldPanel("thank_you", classname="full"),
            ],
            "Page",
        ),
        panels.MultiFieldPanel(
            [
                panels.FieldPanel("to_address"),
                panels.FieldPanel("subject"),
                panels.FieldPanel("email_content", classname="full"),
                panels.FieldPanel("attach_as"),
            ],
            "Email",
        ),
        panels.InlinePanel("form_fields", label="Form fields"),
    ]

    def send_mail(self, form):
        kwargs = {
            "title": self.title.replace(" ", "_"),
            "to_addresses": self.to_address.split(","),
            "field_values": self.get_field_values(form),
            "submission_pk": self.get_submission_class().objects.last().pk,
        }
        if self.attach_as == "xls":
            emails.XlsxFormEmail.send(self, **kwargs)
        elif self.attach_as == "txt":
            emails.TextFormEmail.send(self, **kwargs)
        else:
            emails.FormEmail.send(self, **kwargs)

    def get_field_values(self, form):
        fields = {}
        for field in form:
            value = field.value()
            if isinstance(value, list):
                value = ", ".join(value)
            fields[field.label] = value
        return fields
