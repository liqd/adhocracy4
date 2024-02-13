from argparse import RawTextHelpFormatter

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

from adhocracy4.comments.models import Comment
from meinberlin.apps.ideas.models import Idea


class Command(BaseCommand):
    help = """
    Creates fake comments for testing.
    The command creates <count> comments as <user> on the specified <idea>.
    To generate comments with the fixed text "Fake Comment" specify "--fixed".
    Usage:

        $ ./manage.py create_comments --user <pk> --idea <pk> --count <int>
    """

    def create_parser(self, *args, **kwargs):
        parser = super(Command, self).create_parser(*args, **kwargs)
        parser.formatter_class = RawTextHelpFormatter
        return parser

    def add_arguments(self, parser):
        parser.add_argument(
            "--user",
            default=0,
            type=int,
            required=True,
            help="primary key of user used to create the comments",
        )
        parser.add_argument(
            "--idea",
            default=-1,
            type=int,
            required=True,
            help="primary key of the idea to add the comments to",
        )
        parser.add_argument(
            "--count",
            default=1,
            type=int,
            required=True,
            help="number of comments to create",
        )
        parser.add_argument(
            "--fixed",
            action="store_true",
            help="use fixed comment text",
        )

    def handle(self, *args, **options):
        user_pk = options["user"]
        idea_pk = options["idea"]
        count = options["count"]
        fixed = options["fixed"]

        user_model = get_user_model()
        user = user_model.objects.get(pk=user_pk)
        idea = Idea.objects.get(pk=idea_pk)

        fake = Faker("en_US")

        comments = []
        for i in range(count):
            comments.append(
                Comment(
                    content_object=idea,
                    creator=user,
                    project=idea.project,
                    comment=(
                        fake.text(max_nb_chars=200) if not fixed else "Fake Comment"
                    ),
                )
            )
        Comment.objects.bulk_create(comments)
