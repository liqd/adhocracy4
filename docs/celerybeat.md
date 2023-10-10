## Background

Celery beat enables celery tasks to be scheduled in specific date and time for periodic/repetitive jobs or for scheduling one time tasks

### Configuration

Scheduled tasks are configured via the django admin in Periodic Tasks:
To add/update a new scheduled task:
- go to Periodic Tasks > Periodic tasks - add a new task from top right side.
- give a name for the task
- choose a task from the "Task (registered)"
- tick the enabled box
- add or choose a crontab schedule. [See crontab notation system](https://devhints.io/cron)
- add a start datetime
- check the box for one-off task if the task should run once
- save

### Makefile

We added the makefile command:

- `celery-beat` to start celery beat in the foreground. Requires celery worker to be running, [see](docs/celery.md)
