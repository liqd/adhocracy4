from django.forms.models import BaseInlineFormSet
from django.utils.translation import ugettext_lazy as _


class PhaseInlineFormSet(BaseInlineFormSet):
    def clean(self):
        """
        Make sure phases of the same module don't overlap.
        """
        super().clean()
        phase_dates = []
        for form in self.forms:
            if 'start_date' in form.cleaned_data \
                    and 'end_date' in form.cleaned_data \
                    and form.cleaned_data['start_date'] is not None \
                    and form.cleaned_data['end_date'] is not None:
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                if phase_dates:
                    for phase_date in phase_dates:
                        if (start_date < phase_date[1]
                                and phase_date[0] < end_date):
                            msg = _('Phases cannot run at the same time '
                                    'and must follow after each other.')
                            form.add_error('end_date', msg)
                if start_date and end_date:
                    phase_dates.append((start_date, end_date))
