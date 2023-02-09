from django.core.management.base import BaseCommand

from meinberlin.apps.cms.models import storefronts


class Command(BaseCommand):
    help = "Update item and project counts for the storefront."

    def handle(self, *args, **options):
        for storefront in storefronts.Storefront.objects.all():
            storefront.num_entries = storefronts.get_num_entries_count()
            storefront.num_projects = storefronts.get_num_projects_count()
            storefront.save()
        for item in storefronts.StorefrontItem.objects.filter(district__isnull=False):
            item.district_project_count = item.get_district_project_count()
            item.save()
