import pytest
from django.utils.translation import ugettext as _

from adhocracy4.exports.views import ItemExportView
from adhocracy4.exports.views import SimpleItemExportView

from tests.apps.ideas.models import Idea


def test_simple_item_export_without_setup_fields():

    class SimpleExportView(SimpleItemExportView):
        pass

    with pytest.raises(NotImplementedError):
        SimpleExportView()


def test_simple_item_export_without_export_rows():

    class SimpleExportView(SimpleItemExportView):

        def _setup_fields(self):
            return [], []

    view = SimpleExportView()

    with pytest.raises(NotImplementedError):
        view.export_rows()


def test_simple_item_export_filename():

    class SimpleExportView(SimpleItemExportView):

        def _setup_fields(self):
            return [], []

        def export_rows(self):
            return []

    view = SimpleExportView()

    assert view.get_base_filename().startswith('download')


@pytest.mark.django_db
def test_item_export(idea_factory, module, rf):
    request_ = rf.get('/')
    module_ = module

    class IdeaExportView(ItemExportView):
        model = Idea
        fields = ['name', 'creator', 'created']

        def get_queryset(self):
            return Idea.objects.order_by('id')

        request = request_
        module = module_

    idea0 = idea_factory(module=module)
    idea1 = idea_factory(module=module)

    view = IdeaExportView()

    header = [_('Link')] + [Idea._meta.get_field(name).verbose_name
                            for name in IdeaExportView.fields]
    assert view.get_header() == header

    rows = list(view.export_rows())
    assert len(rows) == 2

    assert rows[0][0].endswith(idea0.get_absolute_url())
    assert rows[0][1] == idea0.name
    assert rows[0][2] == idea0.creator.username
    assert rows[0][3] == idea0.created.isoformat()

    assert rows[1][0].endswith(idea1.get_absolute_url())
    assert rows[1][1] == idea1.name
    assert rows[1][2] == idea1.creator.username
    assert rows[1][3] == idea1.created.isoformat()


@pytest.mark.django_db
def test_item_text_cleanup(idea_factory, module, rf):
    request_ = rf.get('/')
    module_ = module

    class IdeaExportView(ItemExportView):
        model = Idea
        fields = ['description']

        def get_queryset(self):
            return Idea.objects.order_by('id')

        request = request_
        module = module_

    idea_factory(module=module, description='  <i>desc</i>ription ')

    view = IdeaExportView()
    rows = list(view.export_rows())
    assert rows[0][1] == 'description '
