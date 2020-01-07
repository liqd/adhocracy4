from autofixture import AutoFixture
from autofixture import constraints
from autofixture import generators
from autofixture import register
from faker import Factory

from . import content
from . import models

fake = Factory.create()


def only_two_phases_per_module(model, instance):
    if instance.module.phase_set.count() >= 2:
        raise constraints.InvalidConstraint(['module'])


class PhaseAutoFixture(AutoFixture):
    field_values = {
        'name': generators.CallableGenerator(fake.company),
        'type': generators.ChoicesGenerator(choices=content.as_choices()),
    }

    follow_pk = True

    constraints = (
        only_two_phases_per_module
    )


register(models.Phase, PhaseAutoFixture)
