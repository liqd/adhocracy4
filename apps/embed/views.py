from django.views import generic


class EmbedView(generic.base.TemplateView):
    template_name = "meinberlin_embed/embed.html"
