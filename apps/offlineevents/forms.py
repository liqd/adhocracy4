from adhocracy4.categories import forms as category_forms

from . import models


class OfflineEventForm(category_forms.CategorizableForm):

    class Meta:
        model = models.OfflineEvent
        fields = ['name', 'date', 'description']
