from django.views import generic


class ComponentLibraryView(generic.base.TemplateView):
    template_name = 'meinberlin_contrib/component_library.html'
