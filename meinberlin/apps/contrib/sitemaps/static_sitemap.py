from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return ["meinberlin_plans:plan-list"]

    def location(self, obj):
        return reverse(obj)
