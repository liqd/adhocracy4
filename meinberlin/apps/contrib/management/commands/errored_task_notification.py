from background_task.models import CompletedTask
from django.core.management.base import BaseCommand
from django.urls import reverse


class Command(BaseCommand):
    help = 'Send notifications to inform admins about taks that errored'

    def handle(self, *args, **options):
        broken_tasks = CompletedTask\
            .objects.exclude(last_error='')\
            .order_by('-run_at')

        for task in broken_tasks:
            url = reverse(
                'admin:{}_{}_change'.format(
                    task._meta.app_label,
                    task._meta.model_name),
                args=[task.id])
            self.stdout.write(
                'Error in Task {}, see: {} \n'.format(task.task_params, url))
