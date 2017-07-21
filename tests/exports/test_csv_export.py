import csv

import pytest

from meinberlin.apps.exports import views


@pytest.mark.django_db
def test_csv_export(rf, module):
    class CSVExport(views.AbstractCSVExportView):
        def get_filename(self):
            return 'testexport.csv'

        def get_header(self):
            return ['head1', 'head2']

        def export_rows(self):
            return [['regular', 'delimiter,;\t '],
                    ['escaping"\'', 'newlines\r\n']]

    request = rf.get('/')
    response = CSVExport.as_view()(request, module=module)

    assert response['Content-Disposition'] == 'attachment; ' \
                                              'filename="testexport.csv"'

    reader = csv.reader(response.content.decode('utf-8').splitlines(True),
                        lineterminator='\n', quotechar='"',
                        quoting=csv.QUOTE_ALL)
    lines = list(reader)
    assert lines[0] == ['head1', 'head2']
    assert lines[1] == ['regular', 'delimiter,;\t ']
    assert lines[2] == ['escaping"\'', 'newlines\r\n']
