# Timeline

On most platforms using adhocracy4, multiple modules can be added
to a project. There are also offline events than can be added to the
projects. To display the occurence of the module and give a good
overview over the steps of the participation of one project, we
use the following logic:


## Module clusters

-   when there is only one module in a project, the view is dispatched to the module view
-   for more modules, a project view is displayed
-   modules know their start and end date: the first phase start and the last phase end of itself
-   if modules overlap, they are clustered
-   overlapping means, that they share any time; the start of one module is before the end of the other one
-   all overlapping phases are added to the same cluster
-   two modules not overlapping can be in the same cluster, when they both overlap with the same module
-   a cluster can only contain one module


### Module properties concerning the timeline

-   project_modules
    -   all published modules of project
-   other_modules
    -   all published modules of project without itself
-   module_cluster
    -   returns cluster if module is part of one
    -   else returns empty list
-   index_in_cluster
    -   its own index in the module cluster to make nextination work
-   readable_index_in_cluster
    -   used to display number of cluster
-   is_in_module_cluster
-   next_module_in_cluster
    -   for nextination
-   previous_module_in_cluster
    -   for nextination
-   get_timeline_index
    -   index of own cluster in the timeline
-   get_detail_url
    -   if there is only one module in the project, the datail view equals the project view
    -   if the cluster has more than one modules, there is a special module view
    -   if there is only one module, but the timeline is displayed, the project view has to be shown with the corresponsing timeline tile active


## Offline events
Additionally to the modules, which are always some form of online
participation, some of the platforms also have offline events. To
work with the timeline, these need to be implemented as `OfflineEvent`
with `slug, name, date, event_type, description` like in
[adhocracy+](https://github.com/liqd/adhocracy-plus/blob/master/apps/offlineevents/models.py).


## Project properties concerning the timeline
from ModuleClusterPropertiesMixin:
-   module_clusters
-   module_cluster_dict
-   running_modules

from TimelinePropertiesMixin:
-   get_events_list
-   participation_dates
-   display_timeline
-   get_current_participation_date
-   get_current_event
-   get_current_modules

from the properties of Project:
-   end_date
    -   returns end date of project
    - can either be end date of last module or date of last event
-   events
    -   returns all offlineevents
-   has_future_events

There are more module properties in the project's models.py, explained [here](./docs/phases_and_modules.md).


## Timeline

-   module clusters and offline events are displayed in the timeline
-   the timeline is shown when there is more than one module cluster or at least one offline event
