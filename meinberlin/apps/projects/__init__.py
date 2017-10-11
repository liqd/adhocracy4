from functools import lru_cache


@lru_cache(maxsize=32)
def get_project_type(project):
    if (hasattr(project, 'externalproject') and
            hasattr(project.externalproject, 'bplan')):
        return 'bplan'
    elif hasattr(project, 'externalproject'):
        return 'external'
    elif hasattr(project, 'projectcontainer'):
        return 'container'
    else:
        return 'default'
