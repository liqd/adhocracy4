import pytest
from django.utils.translation import ugettext as _

from adhocracy4.ratings.models import Rating
from adhocracy4.exports.views import ItemExportView
from adhocracy4.exports.mixins import ItemExportWithRatesMixin
from adhocracy4.exports.mixins import ItemExportWithCommentCountMixin
from adhocracy4.exports.mixins import ItemExportWithCommentsMixin
from adhocracy4.exports.mixins import ItemExportWithLocationMixin
from tests.apps.ideas.models import Idea


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
    assert rows[0][1] == 'description'
