from django.db.models import Q
from django.utils.translation import gettext_lazy as _


def get_module_clusters(modules):
    modules = (
        modules.filter(is_draft=False)
        .annotate_module_start()
        .annotate_module_end()
        .exclude(Q(module_start=None) | Q(module_end=None))
        .order_by("module_start", "weight")
    )
    clusters = []

    try:
        end_date = modules.first().module_end
        first_cluster = [modules.first()]
        current_cluster = first_cluster
        clusters.append(first_cluster)

        for module in modules[1:]:
            if module.module_start > end_date:
                end_date = module.module_end
                next_cluster = [module]
                current_cluster = next_cluster
                clusters.append(next_cluster)
            else:
                current_cluster.append(module)
                if module.module_end > end_date:
                    end_date = module.module_end
    except AttributeError:
        pass
    return clusters


def get_module_clusters_dict(module_clusters):
    """Build timeline metadata dicts for overlapping module clusters.

    Consumed via ``Project.module_cluster_dict`` and ``participation_dates``.
    Cluster titles are not rendered in adhocracy+ UI (the project-detail
    carousel and module prev/next cluster navigation were removed). The dict
    still backs module URL routing (``get_detail_url`` may append
    ``?initialSlide=``, but project detail no longer reads that param),
    sibling-module sections on module detail, offline-event timeline indices,
    and legacy ``DisplayProjectOrModuleMixin`` context. The visible
    project-detail grid/timeline uses a separate status-based helper in
    adhocracy-plus (``apps.projects.timeline``).
    """

    clusters = []

    for index, cluster in enumerate(module_clusters):
        start_date = cluster[0].module_start
        end_dates = [module.module_end for module in cluster]
        end_date = sorted(end_dates)[-1]
        clusters.append(
            {
                "title": _("{}. Participation").format(str(index + 1)),
                "type": "module",
                "count": index + 1,
                "date": start_date,
                "end_date": end_date,
                "modules": cluster,
            }
        )
    if len(clusters) == 1:
        clusters[0]["title"] = _("Participation")
    return clusters
