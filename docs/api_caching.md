## API Performance

We have noticed that the page load of `mein.berlin.de/projekte/` is pretty slow with about 6s for 550 projects. Three API calls are particularly slow:

- https://mein.berlin.de/api/projects/?status=pastParticipation		2.811s
- https://mein.berlin.de/api/plans/					                      3.613s
- https://mein.berlin.de/api/extprojects/				                  5.041s

These paths correspond to the following api views:

- `projects/api.py::ProjectListViewSet`
- `plans/api.py::PlansListViewSet`
- `extprojects/api.py::ExternalProjectListViewSet`

we decided to start caching the endpoints with redis.

## API Endpoints affected

The cache target is the `list` method of the following views:

- `ExternalProjectListViewSet`
- `PlansListViewSet`
- `ProjectListViewSet`
- `PrivateProjectListViewSet`

Cache keys expire after a timeout (default value 1h) or if a context specific signal is received (e.g. cache keys for projects are deleted if the signal for a saved project is detected).

The cache keys for projects are constructed by the view namespace and their status if exists:
- `projects_activeParticipation`
- `projects_pastParticipation`
- `projects_futureParticipation`
- `privateprojects`
- `extprojects`
- `plans`

## Celery tasks

A periodic task checks for projects that will become either active or past in the next 10 minutes.
- schedule_reset_cache_for_projects()

In case of projects becoming active the cache is cleared for:
- `projects_activeParticipation`
- `projects_futureParticipation`
- `privateprojects`
- `extprojects`

in case of projects becoming past the cache is cleared for:
- `projects_activeParticipation`
- `projects_pastParticipation`
- `privateprojects`
- `extprojects`

In production, we use django's built-in [Redis](https://docs.djangoproject.com/en/4.2/topics/cache/#redis) as cache backend (see `settings/production.py::CACHES`). For development and testing the cache backend is the default, that is [local memory](https://docs.djangoproject.com/en/4.2/topics/cache/#local-memory-caching). If you want to enable redis cache for local development, then copy the production settings to your `settings/local.py`.

files: 
- `./meinberlin/apps/plans/api.py`
- `./meinberlin/apps/extprojects/api.py`
- `./meinberlin/apps/projects/api.py`
- `./meinberlin/apps/projects/tasks.py`
- `./meinberlin/config/settings/production.py`

## Testing

For simulating api performance load, we can create fake projects and plans with the management command `devtools`. The command is part of the `dev` app and can be added in the `meinberlin/config/settings/local.py` settings. It is added by default in the `dev.py` settings.
Usage examples:
```
       $ ./manage.py devtools
       $ ./manage.py devtools --projects 0
       $ ./manage.py devtools --plans 550
       $ ./manage.py devtools --ext-projects 100
```
