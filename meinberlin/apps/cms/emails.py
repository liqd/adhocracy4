import io
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

import xlsxwriter
from django.utils import timezone
from django.utils.translation import ugettext as _

from adhocracy4.emails.mixins import SyncEmailMixin
from meinberlin.apps.contrib.emails import Email


class FormEmail(SyncEmailMixin, Email):
    template_name = 'meinberlin_cms/emails/form_submission'

    def get_receivers(self):
        return [x.strip() for x in self.object.to_address.split(',')]


class XlsxFormEmail(FormEmail):

    def _generate_xlsx(self):
        stream = io.BytesIO()
        workbook = xlsxwriter.Workbook(stream, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        worksheet.write(0, 0, _('Form Field'))
        worksheet.write(0, 1, _('Response'))

        rows = self.object.field_values.items()
        for rownum, row in enumerate(rows, start=1):
            worksheet.write(rownum, 0, row[0])
            worksheet.write(rownum, 1, self._fix_newline_if_string(row[1]))

        workbook.close()
        return stream.getvalue()

    def _fix_newline_if_string(self, value):
        if isinstance(value, str):
            return value.replace('\r', '')
        return value

    def get_attachments(self):
        attachments = super().get_attachments()
        xlsx_data = self._generate_xlsx()
        mime_doc = MIMEApplication(
            _data=xlsx_data,
            _subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        timestamp = timezone.now().strftime("%Y-%m-%d")
        form_title = self.object.title.replace(' ', '_')
        submission_pk = self.object.get_submission_class().objects.last().pk
        filename = '{}_{}_{}.xlsx'.format(timestamp, form_title, submission_pk)
        mime_doc.add_header(
            'Content-Disposition',
            'attachment; filename="{}"'.format(filename)
        )
        return attachments + [mime_doc]


class TextFormEmail(FormEmail):

    def get_attachments(self):
        attachments = super().get_attachments()
        text = ''
        for field, value in self.object.field_values.items():
            text += '{}:\n{}\n\n'.format(field, value)
        mime_doc = MIMEText(_text=text, _charset='utf-8')
        return attachments + [mime_doc]
