from adhocracy4.modules.models import Module
from adhocracy4.phases.models import Phase


def cmp_module_offlineevent(x, y):
    x_date = x.first_phase_start_date if isinstance(x, Module) else x.date
    if x_date is None:
        return 1

    y_date = y.first_phase_start_date if isinstance(y, Module) else y.date
    if y_date is None:
        return -1

    if x_date > y_date:
        return 1
    elif x_date == y_date:
        return 0
    else:
        return -1


def cmp_phase_offlineevent(x, y):
    x_date = x.start_date if isinstance(x, Phase) else x.date
    if x_date is None:
        return 1

    y_date = y.start_date if isinstance(y, Phase) else y.date
    if y_date is None:
        return -1

    if x_date > y_date:
        return 1
    elif x_date == y_date:
        return 0
    else:
        return -1
