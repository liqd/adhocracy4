import csv
import io
from email.mime.text import MIMEText

from django.utils import timezone
from django.utils.translation import ugettext as _

from adhocracy4 import emails as a4_emails


class FormEmail(a4_emails.Email):
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
        csv = MIMEText(_text=csv_text, _subtype='csv')
        timestamp = timezone.now().strftime("%Y-%m-%d")
        form_title = self.object.title.replace(' ', '_')
        filename = '{}_{}.csv'.format(timestamp, form_title)
        csv.add_header(
            'Content-Disposition',
            'attachment; filename="{}"'.format(filename)
        )
        return attachments + [csv]
