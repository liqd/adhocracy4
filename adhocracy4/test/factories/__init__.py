import random

import factory
from dateutil.parser import parse
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.utils.module_loading import import_string

from adhocracy4 import phases
from adhocracy4.administrative_districts.models import AdministrativeDistrict
from adhocracy4.modules.models import Module
from adhocracy4.phases.models import Phase
from adhocracy4.projects.enums import Access
from adhocracy4.projects.models import Project
from adhocracy4.projects.models import Topic


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = factory.Faker("name")


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: "user%d" % n)
    email = factory.Sequence(lambda n: "user%d@liqd.net" % n)
    password = make_password("password")
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


USER_FACTORY = getattr(settings, "A4_USER_FACTORY", UserFactory)


class AdminFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    username = factory.Faker("name")
    password = (  # password = "password"
        "pbkdf2_sha256$20000$"
        "qMYSzezfIiw3$w3A0xY/kOgE8yA4m3RDFItXTqWCV3N7v2CLy2fD8gyw="
    )
    is_superuser = True


ORGANISATION_FACTORY = getattr(settings, "A4_ORGANISATION_FACTORY")


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    name = factory.Faker("sentence", nb_words=4)
    group = factory.SubFactory(GroupFactory)
    slug = factory.Faker("slug")
    organisation = factory.SubFactory(ORGANISATION_FACTORY)
    description = factory.Faker("text", max_nb_chars=120)
    information = factory.Faker("text")
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

    @factory.post_generation
    def topics(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for topic in extracted:
                self.topics.add(topic)


class TopicFactory(factory.django.DjangoModelFactory):
    """Create Topics from the TopicEnum class

    Note: This factory can only create len(TopicEnum) topics because of the unique
    constraint of the Topic model
    """

    class Meta:
        model = Topic

    code = factory.Sequence(lambda n: TopicFactory.get_topic_from_enum(n))

    @factory.post_generation
    def projects(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for project in extracted:
                self.project_set.add(project)

    @staticmethod
    def get_topic_from_enum(i):
        if hasattr(settings, "A4_PROJECT_TOPICS"):
            topics_enum = import_string(settings.A4_PROJECT_TOPICS)
            return topics_enum.names[i]
        return str(i)


class ModuleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Module

    name = factory.Faker("sentence", nb_words=4)
    slug = factory.Faker("slug")
    description = factory.Faker("text")
    weight = random.randint(1, 1000)
    project = factory.SubFactory(ProjectFactory)


class ItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True

    module = factory.SubFactory(ModuleFactory)
    creator = factory.SubFactory(USER_FACTORY)


class PhaseContentFactory(factory.Factory):
    class Meta:
        model = phases.PhaseContent

    app = "phase_content_factory"
    phase = "factory_phase"
    view = None

    name = "Factory Phase"
    description = "Factory Phase Description"
    module_name = "factory phase module"

    features = {}

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        phase_content = model_class()
        for key, value in kwargs.items():
            setattr(phase_content, key, value)

        phases.content.register(phase_content)
        return phase_content


class PhaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Phase

    class Params:
        phase_content = PhaseContentFactory()

    name = factory.Sequence(lambda n: "{}. phase".format(n))
    description = factory.Faker("text")
    module = factory.SubFactory(ModuleFactory)
    start_date = parse("2013-01-02 00:00:00 UTC")
    end_date = parse("2013-01-03 00:00:00 UTC")

    type = factory.LazyAttribute(lambda f: f.phase_content.identifier)


class SettingsFactory(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True

    module = factory.SubFactory(ModuleFactory)


class AdministrativeDistrictFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AdministrativeDistrict

    name = factory.Faker("name")
