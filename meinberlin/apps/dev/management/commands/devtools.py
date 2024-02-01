from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db.models import QuerySet

from adhocracy4.administrative_districts.models import AdministrativeDistrict
from adhocracy4.projects.enums import Access
from meinberlin.apps.extprojects.models import ExternalProject
from meinberlin.apps.organisations.models import Organisation
from meinberlin.apps.plans.models import Plan
from meinberlin.apps.projects.models import Project
from meinberlin.apps.users.models import User


class Command(BaseCommand):
    help = """
    Creates fake data for testing API performance.

    The command on its own counts fake objects currently in the database and prints a summary.

    The argument --plans makes sure that at exactly n fake plans exist.
    The argument --projects makes sure that at exactly n fake projects exist.
    The argument --ext-projects makes sure that at exactly n fake external projects exist.

    Usage:

        $ ./manage.py devtools
        $ ./manage.py devtools --projects 0
        $ ./manage.py devtools --plans 550
        $ ./manage.py devtools --ext-projects 100
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--plans",
            default=-1,
            type=int,
            help="number of fake plans to have in database",
        )
        parser.add_argument(
            "--projects",
            default=-1,
            type=int,
            help="number of fake projects to have in database",
        )
        parser.add_argument(
            "--ext-projects",
            default=-1,
            type=int,
            help="number of fake external projects to have in database",
        )
        parser.add_argument(
            "--delete",
            action="store_true",
            default=False,
            help="remove all fake data",
        )

    def handle(self, *args, **options):
        for key, model, identifier in [
            ("plans", Plan, "title"),
            ("projects", Project, "name"),
            ("ext_projects", ExternalProject, "name"),
        ]:
            identifier_prefix = f"fake {key.rstrip('s')}"
            fake_objects = model.objects.filter(
                **{f"{identifier}__startswith": identifier_prefix}
            )
            count = fake_objects.count()
            print(f"fake {key} in database: {count=}")

            if options["delete"]:
                deleted, count = fake_objects.delete()
                print(f"deleted fake {key}: {deleted=}, {count=}")

            if options[key] < 0:
                continue

            self.run(
                n_target=options[key],
                key=key,
                identifier_prefix=identifier_prefix,
                fake_objects=fake_objects,
            )

    @staticmethod
    def run(n_target: int, key: str, identifier_prefix: str, fake_objects: QuerySet):
        if n_target == 0:
            deleted, count = fake_objects.delete()
            print(f"deleted fake {key}: {deleted=}, {count=}")

        elif n_target > 0:
            n_current = fake_objects.count()
            n_todo = n_target - n_current

            if n_todo == 0:
                print(f"nothing to do: {n_target=}, {n_current=}")

            elif n_todo > 0:
                print(f"need to create additional fake {key}: {n_todo}")
                if key == "plans":
                    create_fake_plans(n=n_todo, identifier_prefix=identifier_prefix)
                elif key == "projects":
                    create_fake_projects(n=n_todo, identifier_prefix=identifier_prefix)
                elif key == "ext_projects":
                    create_fake_external_projects(
                        n=n_todo, identifier_prefix=identifier_prefix
                    )

                print(f"created fake {key}: {n_todo}")

            elif n_todo < 0:
                n_todo = -n_todo
                print(f"need to delete fake {key}: {n_todo}")
                deleted, count = fake_objects.filter(
                    pk__in=fake_objects.values_list("pk")[:n_todo]
                ).delete()
                print(f"deleted fake {key}: {deleted=}, {count=}")


def create_fake_external_projects(
    n: int,
    identifier_prefix: str,
):
    group = Group.objects.first()
    organisation = Organisation.objects.first()

    for i in range(n):
        project = ExternalProject(
            name=f"{identifier_prefix} {i}",
            group=group,
            organisation=organisation,
            description="fake project description",
            information="fake project information",
            access=Access.PUBLIC,
            is_draft=False,
        )
        project.save()


def create_fake_projects(
    n: int,
    identifier_prefix: str,
):
    group = Group.objects.first()
    organisation = Organisation.objects.first()

    projects = []
    for i in range(n):
        project = Project(
            name=f"{identifier_prefix} {i :0>3}",
            group=group,
            organisation=organisation,
            description="fake project description",
            information="fake project information",
            access=Access.PUBLIC,
            is_draft=False,
        )
        projects.append(project)

    Project.objects.bulk_create(projects)


def create_fake_plans(
    n: int,
    identifier_prefix: str,
):
    user = User.objects.filter(username__contains="admin").first()
    if not user:
        user = User.objects.first()
    organisation = user.organisations.first()
    if not organisation:
        organisation = Organisation.objects.first()
        user.organisation_set.add(organisation)
        user.save()
    district = AdministrativeDistrict.objects.first()

    plans = []
    for i in range(n):
        plan = Plan(
            title=f"{identifier_prefix} {i :0>3}",
            creator=user,
            organisation=organisation,
            district=district,
            point={
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Point",
                    "coordinates": [13.447437286376953, 52.51518602243137],
                },
            },
            contact_address_text="",
            status=Plan.STATUS_ONGOING,
            participation=Plan.PARTICIPATION_INFORMATION,
            is_draft=False,
        )

        plans.append(plan)

    Plan.objects.bulk_create(plans)
