from django.utils.translation import ugettext_lazy as _

from adhocracy4.dashboard.blueprints import ProjectBlueprint
from tests.apps.questions import phases as question_phases

blueprints = [
    ('questions',
     ProjectBlueprint(
         title='Questions',
         description=_(
             'Collect questions first and rate them afterwards.'
         ),
         content=[
             question_phases.AskPhase(),
             question_phases.RatePhase(),
         ],
         image='images/questions.svg',
         settings_model=None,
     )),

]
