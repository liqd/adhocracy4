from django.views import generic
from django.views.decorators.clickjacking import xframe_options_exempt


class EmbedView(generic.base.TemplateView):
    template_name = "meinberlin_embed/embed.html"

    @xframe_options_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
