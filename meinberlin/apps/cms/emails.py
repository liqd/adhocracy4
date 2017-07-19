import csv
import io
from email.mime.text import MIMEText

from django.utils import timezone
from django.utils.translation import ugettext as _

from meinberlin.apps.contrib.emails import Email


class FormEmail(Email):
    template_name = 'meinberlin_cms/emails/form_submission'

    def get_receivers(self):
        return [x.strip() for x in self.object.to_address.split(',')]


class CsvFormEmail(FormEmail):

    def _generate_csv(self):
        stream = io.StringIO()
        fw = csv.writer(stream, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        fw.writerow([_('Form Field'), _('Response')])
        for field, value in self.object.field_values.items():
            fw.writerow([field, value])
        return stream.getvalue()

    def get_attachments(self):
        attachments = super().get_attachments()
        csv_text = self._generate_csv()
        mime_doc = MIMEText(_text=csv_text, _subtype='csv', _charset='utf-8')
        timestamp = timezone.now().strftime("%Y-%m-%d")
        form_title = self.object.title.replace(' ', '_')
        submission_pk = self.object.get_submission_class().objects.last().pk
        filename = '{}_{}_{}.csv'.format(timestamp, form_title, submission_pk)
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
