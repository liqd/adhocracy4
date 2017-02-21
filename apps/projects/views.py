from django.utils.translation import ugettext as _

from adhocracy4.contrib.views import SortableListView
from adhocracy4.projects import models


class ProjectListView(SortableListView):
    model = models.Project
    paginate_by = 16
    ordering = ['-created']
    orderings_supported = [
        ('-created', _('Most recent')),
    ]
