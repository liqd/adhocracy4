## Background

We have noticed that the page load of `mein.berlin.de/projekte/` is pretty slow with about 6s for 550 projects. Three API calls are particularly slow:

- https://mein.berlin.de/api/projects/?status=pastParticipation		2.811s
- https://mein.berlin.de/api/plans/					                      3.613s
- https://mein.berlin.de/api/extprojects/				                  5.041s

These paths correspond to the following api views:

- `projects/api.py::ProjectListViewSet`
- `plans/api.py::PlansListViewSet`
- `extprojects/api.py::ExternalProjectListViewSet`

we decided to start caching the endpoints with a redis backend.

## Developer Notes

The cache target is the `list` method of the following views:

- `ExternalProjectListViewSet`
- `PlansListViewSet`
- `ProjectListViewSet`
- `PrivateProjectListViewSet`

Cache keys expire after a timeout (default value 1h) or if a context specific signal is received (e.g. cache keys for projects are deleted if the signal for a saved project is detected).

The cache keys for projects are constructed by the view namespace and their status if exists:
- `projects`
- `projects_activeParticipation`
- `projects_pastParticipation`
- `projects_futureParticipation`
- `privateprojects`
- `extprojects`
- `plans`

In production, we use django's built-in [Redis](https://docs.djangoproject.com/en/4.2/topics/cache/#redis) as cache backend (see `settings/production.py::CACHES`). For development and testing the cache backend is the default, that is [local memory](https://docs.djangoproject.com/en/4.2/topics/cache/#local-memory-caching). If you want to enable redis cache for local development, then copy the production settings to your `settings/local.py`.
