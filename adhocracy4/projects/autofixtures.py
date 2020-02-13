from autofixture import AutoFixture
from autofixture import generators
from autofixture import register
from faker import Factory

from .models import Project

fake = Factory.create()

IMAGESIZES = ((1300, 600),)


class ProjectAutoFixture(AutoFixture):

    field_values = {
        'name': generators.CallableGenerator(fake.company),
        'slug': generators.CallableGenerator(fake.slug),
        'image': generators.ImageGenerator(sizes=IMAGESIZES),
        'is_draft': generators.ChoicesGenerator(values=[True, False, False]),
    }


register(Project, ProjectAutoFixture)
