from functools import lru_cache


@lru_cache()
def get_exports(project_or_module):
    exports = []
    existing_views = set()
    for phase in project_or_module.phases:
        phase_view = phase.content().view
        if hasattr(phase_view, 'exports'):
            for name, view in phase_view.exports:
                if view not in existing_views:
                    existing_views.add(view)
                    exports.append((name, view))
    return exports
