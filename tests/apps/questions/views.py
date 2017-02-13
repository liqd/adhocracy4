from adhocracy4.contrib.views import SortableListView
from . import models


class QuestionList(SortableListView):
    model = models.Question
    ordering = ['-created']
    orderings_supported = [
        ('-created', 'Most recent'),
        ('text', 'Alphabetical'),
    ]
