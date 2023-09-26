
## Background

We have noticed that the page load of `mein.berlin.de/projekte/` is pretty slow with about 6s for 550 projects. Three API calls are particularly slow:

- https://mein.berlin.de/api/projects/?status=pastParticipation		2.811s
- https://mein.berlin.de/api/plans/					                      3.613s
- https://mein.berlin.de/api/extprojects/				                  5.041s

These urls correspond to the following api views:

- `projects/api.py::ProjectListViewSet`
- `plans/api.py::PlansListViewSet`
- `extprojects/api.py::ExternalProjectListViewSet`

And within those we found that we can improve the following field by prefetching:

- `plans/serializers.py::PlanSerializer.get_published_projects_count()`

For the other serializers we could not find any improvements and will resort to caching in a future story.

## Developer Notes

- added a prefetch for the projects that are related to plans (`apps/plans/api::get_queryset`)
- changed the plans serializer so that it counts published projects in Python (faster than hitting database since projects are now prefetched)
