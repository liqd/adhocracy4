from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from meinberlin.apps.users.models import User


class Command(BaseCommand):
    help = 'Remove all users that registered more than n days ago but never ' \
        'logged in. This implies they never verified their email or ' \
        'added an external / social account'

    def add_arguments(self, parser):
        parser.add_argument('days')
        parser.add_argument('test')

    def handle(self, *args, **options):
        test = options['test'] != "False"
        days = int(options['days'])

        all_users = User.objects.all()

        qs = User.objects.filter(last_login=None,
                                 date_joined__lt=(
                                     timezone.now() - timedelta(days=days)))
        if qs:
            print("Users: {} Removing: {} Left: {}".format(
                all_users.count(), qs.count(), all_users.count() - qs.count()))
        for user in qs:
            if test:
                print("Would remove user {} (date_joined: {})".format(
                    user.username, user.date_joined
                ))
            else:
                print("Removing user {} (date_joined: {})".format(
                    user.username, user.date_joined
                ))
                qs.delete()
