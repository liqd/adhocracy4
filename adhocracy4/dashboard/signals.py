from django import dispatch

project_created = dispatch.Signal(providing_args=['project', 'user'])
module_created = dispatch.Signal(providing_args=['module', 'user'])
# Handlers may return an error message to prevent a project from publishing
project_pre_publish = dispatch.Signal(providing_args=['project', 'user'])
project_published = dispatch.Signal(providing_args=['project', 'user'])
project_unpublished = dispatch.Signal(providing_args=['project', 'user'])
module_published = dispatch.Signal(providing_args=['module', 'user'])
module_unpublished = dispatch.Signal(providing_args=['module', 'user'])
project_component_updated = dispatch.Signal(
    providing_args=['project', 'component', 'user'])
module_component_updated = dispatch.Signal(
    providing_args=['module', 'component', 'user'])
