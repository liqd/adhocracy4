from io import BytesIO

import factory
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.files import base
from django.core.files import images
from PIL import Image

from adhocracy4.test import factories


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = settings.AUTH_USER_MODEL

    username = factory.Faker('name')
    password = make_password('password')
    email = factory.Faker('email')


class AdminFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = settings.AUTH_USER_MODEL

    username = factory.Faker('name')
    password = make_password('password')
    is_superuser = True


class PhaseFactory(factories.PhaseFactory):
    type = 'meinberlin_ideas:010:issue'


class OrganisationFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'meinberlin_organisations.Organisation'
        django_get_or_create = ('name',)

    name = factory.Faker('company')

    @factory.post_generation
    def initiators(self, create, extracted, **kwargs):
        if not extracted:
            user = UserFactory()
            self.initiators.add(user)
            return

        if extracted:
            for user in extracted:
                self.initiators.add(user)


class ContentTypeFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'contenttypes.ContentType'

    app_label = factory.Faker('name')
    model = factory.Faker('name')
    name = factory.Faker('name')


class ImageFactory():
    """Create a django file object containg an image."""

    def __call__(self, resolution, image_format='JPEG', name=None):

        filename = name or 'default.{}'.format(image_format.lower())
        color = 'blue'
        image = Image.new('RGB', resolution, color)
        image_data = BytesIO()
        image.save(image_data, image_format)
        image_content = base.ContentFile(image_data.getvalue())
        return images.ImageFile(image_content.file, filename)
