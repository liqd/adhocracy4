from django import dispatch

project_created = dispatch.Signal(providing_args=['project'])
module_created = dispatch.Signal(providing_args=['module'])
# Handlers may return an error message to prevent a project from publishing
project_pre_publish = dispatch.Signal(providing_args=['project'])
project_published = dispatch.Signal(providing_args=['project'])
project_unpublished = dispatch.Signal(providing_args=['project'])
project_archived = dispatch.Signal(providing_args=['project'])
