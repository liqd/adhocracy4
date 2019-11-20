from functools import lru_cache

default_app_config = 'meinberlin.apps.projects.apps.Config'


@lru_cache(maxsize=32)
def get_project_type(project):
    if (project.project_type == '﻿meinberlin_bplan.Bplan'):
        return 'bplan'
    elif (project.project_type ==
            ('﻿meinberlin_extprojects.'
             'ExternalProject')):
        return 'external'
    elif (project.project_type ==
            ('﻿meinberlin_projectcontainers.'
             'ProjectContainer')):
        return 'container'
    else:
        return 'default'
