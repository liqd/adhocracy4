from django.db.models import Q
from django.utils.translation import ugettext_lazy as _


def get_module_clusters(modules):
    modules = modules \
        .filter(is_draft=False) \
        .annotate_module_start() \
        .annotate_module_end() \
        .exclude(Q(module_start=None) | Q(module_end=None)) \
        .order_by('module_start', 'weight')
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

    clusters = []

    for index, cluster in enumerate(module_clusters):
        start_date = cluster[0].module_start
        end_dates = [module.module_end for module in cluster]
        end_date = sorted(end_dates)[-1]
        clusters.append(
            {
                'title': _('{}. Online Participation').format(str(index + 1)),
                'type': 'module',
                'count': index + 1,
                'date': start_date,
                'end_date': end_date,
                'modules': cluster
            }
        )
    if len(clusters) == 1:
        clusters[0]['title'] = _('Online Participation')
    return clusters
