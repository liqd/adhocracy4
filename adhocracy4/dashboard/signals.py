from django import dispatch

# providing: project <-> user
project_created = dispatch.Signal()
# providing: module <-> user
module_created = dispatch.Signal()
# Handlers may return an error message to prevent a project from publishing
# providing: project <-> user
project_pre_publish = dispatch.Signal()
# providing: project <-> user
project_published = dispatch.Signal()
# providing: project <-> user
project_unpublished = dispatch.Signal()
# providing: module <-> user
module_published = dispatch.Signal()
# providing: module <-> user
module_unpublished = dispatch.Signal()
# providing: project <-> component <-> user
project_component_updated = dispatch.Signal()
# providing: project <-> component <-> user
module_component_updated = dispatch.Signal()
