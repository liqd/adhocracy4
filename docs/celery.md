## Background

We want to upgrade Django from the current version to at least 4. But our current approach to running background tasks, namely `django-background-tasks` is no longer supported in Django 4. Hence, we decided to switch to celery for distributed tasks.

## Developer Notes

### configuration

The celery configuration file is `meinberlin/config/celery.py`.

Currently, we make use of the following config parameters:

- `broker_url = "redis://localhost:6379"`
- `result_backend = "redis"`
- `broker_connection_retry_on_startup = True`
- `result_extended = True`

The celery app is configured from the django settings file and namespaced variables. The defaults are defined in `config/settings/base.py` but can be overriden by `config/settings/local.py`.

Note that the default settings in`dev.py` enable the "always eager mode" (`CELERY_TASK_ALWAYS_EAGER = True`) in which the django server will run the shared tasks itself. This is to keep the development setup as lightweight as possible. If you want to develop or test using a celery worker make sure that you add the following to your `local.py`:

```
CELERY_TASK_ALWAYS_EAGER = False
```

and install and run the redis server on your system.

### tasks

Celery is set up to autodiscover tasks. To register a task import the shared task decorator from celery and apply it to your task function.

```python
from celery import shared_task

@shared_task
def add_two_numbers():
    return 1 + 1
```

For testing purposes we have added a dummy task the prints and returns the string `"hello world"`. The dummy task can be called form the celery CLI via

```
$ celery --app meinberlin call dummy_task
b5351175-335d-4be0-b1fa-06278a613ccf
```

### makefile

We added three makefile commands:

- `celery-worker-start` to start a worker node in the foreground
- `celery-worker-status` to inspect registered tasks and running worker nodes
- `celery-worker-dummy-task` to call the dummy task
