from django.contrib.sitemaps import Sitemap
from django.db.models import Q

from adhocracy4.projects.enums import Access
from adhocracy4.projects.models import Project


class Adhocracy4Sitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Project.objects.filter(
            Q(access=Access.PUBLIC) | Q(access=Access.SEMIPUBLIC),
            is_draft=False)
