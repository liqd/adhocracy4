import pytest
from django.utils.translation import ugettext as _

from adhocracy4.exports.views import AbstractXlsxExportView
from adhocracy4.exports.views import BaseExport
from adhocracy4.exports.views import MultipleObjectExport


from tests.apps.ideas.models import Idea


@pytest.mark.django_db
def test_base_export(idea_factory, module):
    idea0 = idea_factory(module=module)
    idea1 = idea_factory(module=module)

    class IdeaExport(BaseExport):
        def get_object_list(self):
            return [idea0, idea1]

        def get_virtual_fields(self, virtual):
            virtual['name'] = 'Name'
            return super().get_virtual_fields(virtual)

        def get_name_data(self, item):
            return item.name

    export = IdeaExport()
    assert export.get_header() == ['Name']

    rows = list(export.export_rows())
    assert len(rows) == 2

    assert rows[0][0] == idea0.name
    assert rows[1][0] == idea1.name


@pytest.mark.django_db
def test_multiple_object_export(idea_factory, module, rf):
    class IdeaExport(MultipleObjectExport):
        model = Idea
        fields = ['description']

        def get_queryset(self):
            return Idea.objects.order_by('id')

        def get_virtual_fields(self, virtual):
            virtual['name'] = 'Name'
            return super().get_virtual_fields(virtual)

        def get_name_data(self, item):
            return item.name

        request = rf.get('/')

    idea0 = idea_factory(module=module)
    idea1 = idea_factory(module=module)

    export = IdeaExport()

    header = [_('Link'),
              Idea._meta.get_field('description').verbose_name,
              'Name']
    assert export.get_header() == header

    rows = list(export.export_rows())
    assert len(rows) == 2

    assert rows[0][0].endswith(idea0.get_absolute_url())
    assert rows[0][1] == idea0.description
    assert rows[0][2] == idea0.name

    assert rows[1][0].endswith(idea1.get_absolute_url())
    assert rows[1][1] == idea1.description
    assert rows[1][2] == idea1.name


def test_xlsx_export_view(rf):
    class XlsxExportView(AbstractXlsxExportView):
        def get_base_filename(self):
            return 'download'

        def get_header(self):
            return ['head1', 'head2']

        def export_rows(self):
            return [('row1col1', 'row1col2'),
                    ('row2col1', 'row2col2')]

    view = XlsxExportView.as_view()
    request = rf.get('/')
    response = view(request)

    assert response.status_code == 200
    assert 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'\
           == response['Content-Type']
    assert 'attachment; filename="download.xlsx"'\
           == response['Content-Disposition']
