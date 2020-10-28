import random

import factory
from dateutil.parser import parse
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

from adhocracy4.administrative_districts.models import AdministrativeDistrict
from adhocracy4.modules.models import Module
from adhocracy4.phases.models import Phase
from adhocracy4.projects.enums import Access
from adhocracy4.projects.models import Project


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = factory.Faker('name')


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'user%d' % n)
    email = factory.Sequence(lambda n: 'user%d@liqd.net' % n)
    password = make_password('password')
    is_staff = False
    is_superuser = False

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.groups.add(group)


USER_FACTORY = getattr(settings, 'A4_USER_FACTORY', UserFactory)


class AdminFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = settings.AUTH_USER_MODEL

    username = factory.Faker('name')
    password = (  # password = "password"
        "pbkdf2_sha256$20000$"
        "qMYSzezfIiw3$w3A0xY/kOgE8yA4m3RDFItXTqWCV3N7v2CLy2fD8gyw="
    )
    is_superuser = True


ORGANISATION_FACTORY = getattr(settings, 'A4_ORGANISATION_FACTORY')


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    name = factory.Faker('sentence', nb_words=4)
    group = factory.SubFactory(GroupFactory)
    slug = factory.Faker('slug')
    organisation = factory.SubFactory(ORGANISATION_FACTORY)
    description = factory.Faker('text', max_nb_chars=120)
    information = factory.Faker('text')
    access = Access.PUBLIC
    is_draft = False

    @factory.post_generation
    def moderators(self, create, extracted, **kwargs):
        if not extracted:
            user_factory = factory.SubFactory(USER_FACTORY).get_factory()
            self.moderators.add(user_factory())
            return

        if extracted:
            for user in extracted:
                self.moderators.add(user)


class ModuleFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Module

    name = factory.Faker('sentence', nb_words=4)
    slug = factory.Faker('slug')
    description = factory.Faker('text')
    weight = random.randint(1, 1000)
    project = factory.SubFactory(ProjectFactory)


class ItemFactory(factory.django.DjangoModelFactory):

    class Meta:
        abstract = True

    module = factory.SubFactory(ModuleFactory)
    creator = factory.SubFactory(USER_FACTORY)


class PhaseFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Phase

    name = factory.Sequence(lambda n: '{}. phase'.format(n))
    description = factory.Faker('text')
    type = 'a4test_questions:ask'
    module = factory.SubFactory(ModuleFactory)
    start_date = parse('2013-01-02 00:00:00 UTC')
    end_date = parse('2013-01-03 00:00:00 UTC')


class SettingsFactory(factory.django.DjangoModelFactory):

    class Meta:
        abstract = True

    module = factory.SubFactory(ModuleFactory)


class AdministrativeDistrictFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = AdministrativeDistrict

    name = factory.Faker('name')
