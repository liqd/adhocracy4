import io
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

import xlsxwriter
from django.utils import timezone
from django.utils.translation import gettext as _

from meinberlin.apps.contrib.emails import Email


class FormEmail(Email):
    template_name = "meinberlin_cms/emails/form_submission"

    def get_receivers(self):
        return [x.strip() for x in self.kwargs.get("to_addresses")]


class FormEmailAttached(FormEmail):
    template_name = "meinberlin_cms/emails/form_submission_attached"


class XlsxFormEmail(FormEmailAttached):
    def _generate_xlsx(self):
        stream = io.BytesIO()
        workbook = xlsxwriter.Workbook(
            stream, {"in_memory": True, "strings_to_formulas": False}
        )
        worksheet = workbook.add_worksheet()

        worksheet.write(0, 0, _("Form Field"))
        worksheet.write(0, 1, _("Response"))

        field_values = self.kwargs.get("field_values")
        for rownum, row in enumerate(field_values.items(), start=1):
            worksheet.write(rownum, 0, row[0])
            worksheet.write(rownum, 1, self._fix_newline_if_string(row[1]))

        workbook.close()
        return stream.getvalue()

    def _fix_newline_if_string(self, value):
        if isinstance(value, str):
            return value.replace("\r", "")
        return value

    def get_attachments(self):
        attachments = super().get_attachments()
        xlsx_data = self._generate_xlsx()
        mime_doc = MIMEApplication(
            _data=xlsx_data,
            _subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        timestamp = timezone.now().strftime("%Y-%m-%d")
        form_title = self.kwargs.get("title")
        submission_pk = self.kwargs.get("submission_pk")
        filename = "{}_{}_{}.xlsx".format(timestamp, form_title, submission_pk)
        mime_doc.add_header(
            "Content-Disposition", 'attachment; filename="{}"'.format(filename)
        )
        return attachments + [mime_doc]


class TextFormEmail(FormEmailAttached):
    def get_attachments(self):
        attachments = super().get_attachments()
        text = ""
        field_values = self.kwargs.get("field_values")
        for field, value in field_values.items():
            text += "{}:\n{}\n\n".format(field, value)
        mime_doc = MIMEText(_text=text, _charset="utf-8")
        timestamp = timezone.now().strftime("%Y-%m-%d")
        form_title = self.kwargs.get("title")
        submission_pk = self.kwargs.get("submission_pk")
        filename = "{}_{}_{}.txt".format(timestamp, form_title, submission_pk)
        mime_doc.add_header(
            "Content-Disposition", 'attachment; filename="{}"'.format(filename)
        )
        return attachments + [mime_doc]
