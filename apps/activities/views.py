from django.views import generic

from .models import Activity


class AllActivitiesView(generic.ListView):
    model = Activity
